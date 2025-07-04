# Copyright (c) 2023, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import inspect

import nts 
from nts  import _, qb
from nts .model.document import Document
from nts .utils.data import comma_and

from prodman.stock import get_warehouse_account_map


class RepostAccountingLedger(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.repost_accounting_ledger_items.repost_accounting_ledger_items import (
			RepostAccountingLedgerItems,
		)

		amended_from: DF.Link | None
		company: DF.Link | None
		delete_cancelled_entries: DF.Check
		vouchers: DF.Table[RepostAccountingLedgerItems]
	# end: auto-generated types

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._allowed_types = get_allowed_types_from_settings()

	def validate(self):
		self.validate_vouchers()
		self.validate_for_closed_fiscal_year()
		self.validate_for_deferred_accounting()

	def validate_for_deferred_accounting(self):
		sales_docs = [x.voucher_no for x in self.vouchers if x.voucher_type == "Sales Invoice"]
		purchase_docs = [x.voucher_no for x in self.vouchers if x.voucher_type == "Purchase Invoice"]
		validate_docs_for_deferred_accounting(sales_docs, purchase_docs)

	def validate_for_closed_fiscal_year(self):
		if self.vouchers:
			latest_pcv = (
				nts .db.get_all(
					"Period Closing Voucher",
					filters={"company": self.company, "docstatus": 1},
					order_by="period_end_date desc",
					pluck="period_end_date",
					limit=1,
				)
				or None
			)
			if not latest_pcv:
				return

			for vtype in self._allowed_types:
				if names := [x.voucher_no for x in self.vouchers if x.voucher_type == vtype]:
					latest_voucher = nts .db.get_all(
						vtype,
						filters={"name": ["in", names]},
						pluck="posting_date",
						order_by="posting_date desc",
						limit=1,
					)[0]
					if latest_voucher and latest_pcv[0] >= latest_voucher:
						nts .throw(_("Cannot Resubmit Ledger entries for vouchers in Closed fiscal year."))

	def validate_vouchers(self):
		if self.vouchers:
			validate_docs_for_voucher_types([x.voucher_type for x in self.vouchers])

	def get_existing_ledger_entries(self):
		vouchers = [x.voucher_no for x in self.vouchers]
		gl = qb.DocType("GL Entry")
		existing_gles = (
			qb.from_(gl)
			.select(gl.star)
			.where((gl.voucher_no.isin(vouchers)) & (gl.is_cancelled == 0))
			.run(as_dict=True)
		)
		self.gles = nts ._dict({})

		for gle in existing_gles:
			self.gles.setdefault((gle.voucher_type, gle.voucher_no), nts ._dict({})).setdefault(
				"existing", []
			).append(gle.update({"old": True}))

	def generate_preview_data(self):
		nts .flags.through_repost_accounting_ledger = True
		self.gl_entries = []
		self.get_existing_ledger_entries()
		for x in self.vouchers:
			doc = nts .get_doc(x.voucher_type, x.voucher_no)
			if doc.doctype in ["Payment Entry", "Journal Entry"]:
				gle_map = doc.build_gl_map()
			elif doc.doctype == "Purchase Receipt":
				warehouse_account_map = get_warehouse_account_map(doc.company)
				gle_map = doc.get_gl_entries(warehouse_account_map)
			else:
				gle_map = doc.get_gl_entries()

			old_entries = self.gles.get((x.voucher_type, x.voucher_no))
			if old_entries:
				self.gl_entries.extend(old_entries.existing)
			self.gl_entries.extend(gle_map)

	@nts .whitelist()
	def generate_preview(self):
		from prodman.accounts.report.general_ledger.general_ledger import get_columns as get_gl_columns

		gl_columns = []
		gl_data = []

		self.generate_preview_data()
		if self.gl_entries:
			filters = {"company": self.company, "include_dimensions": 1}
			for x in get_gl_columns(filters):
				if x["fieldname"] == "gl_entry":
					x["fieldname"] = "name"
				gl_columns.append(x)

			gl_data = self.gl_entries
		rendered_page = nts .render_template(
			"prodman/accounts/doctype/repost_accounting_ledger/repost_accounting_ledger.html",
			{"gl_columns": gl_columns, "gl_data": gl_data},
		)

		return rendered_page

	def on_submit(self):
		if len(self.vouchers) > 5:
			job_name = "repost_accounting_ledger_" + self.name
			nts .enqueue(
				method="prodman.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger.start_repost",
				account_repost_doc=self.name,
				is_async=True,
				job_name=job_name,
			)
			nts .msgprint(_("Repost has started in the background"))
		else:
			start_repost(self.name)


@nts .whitelist()
def start_repost(account_repost_doc=str) -> None:
	from prodman.accounts.general_ledger import make_reverse_gl_entries

	nts .flags.through_repost_accounting_ledger = True
	if account_repost_doc:
		repost_doc = nts .get_doc("Repost Accounting Ledger", account_repost_doc)

		if repost_doc.docstatus == 1:
			# Prevent repost on invoices with deferred accounting
			repost_doc.validate_for_deferred_accounting()

			for x in repost_doc.vouchers:
				doc = nts .get_doc(x.voucher_type, x.voucher_no)

				if repost_doc.delete_cancelled_entries:
					nts .db.delete(
						"GL Entry", filters={"voucher_type": doc.doctype, "voucher_no": doc.name}
					)
					nts .db.delete(
						"Payment Ledger Entry", filters={"voucher_type": doc.doctype, "voucher_no": doc.name}
					)

				if doc.doctype in ["Sales Invoice", "Purchase Invoice"]:
					if not repost_doc.delete_cancelled_entries:
						doc.docstatus = 2
						doc.make_gl_entries_on_cancel()

					doc.docstatus = 1
					if doc.doctype == "Sales Invoice":
						doc.force_set_against_income_account()
					else:
						doc.force_set_against_expense_account()
					doc.make_gl_entries()

				elif doc.doctype == "Purchase Receipt":
					if not repost_doc.delete_cancelled_entries:
						doc.docstatus = 2
						doc.make_gl_entries_on_cancel()

					doc.docstatus = 1
					doc.make_gl_entries(from_repost=True)

				elif doc.doctype in ["Payment Entry", "Journal Entry", "Expense Claim"]:
					if not repost_doc.delete_cancelled_entries:
						doc.make_gl_entries(1)
					doc.make_gl_entries()
				elif doc.doctype in nts .get_hooks("repost_allowed_doctypes"):
					if hasattr(doc, "make_gl_entries") and callable(doc.make_gl_entries):
						if not repost_doc.delete_cancelled_entries:
							if "cancel" in inspect.getfullargspec(doc.make_gl_entries):
								doc.make_gl_entries(cancel=1)
							else:
								make_reverse_gl_entries(voucher_type=doc.doctype, voucher_no=doc.name)
						doc.make_gl_entries()


def get_allowed_types_from_settings():
	return [
		x.document_type
		for x in nts .db.get_all(
			"Repost Allowed Types", filters={"allowed": True}, fields=["distinct(document_type)"]
		)
	]


def validate_docs_for_deferred_accounting(sales_docs, purchase_docs):
	docs_with_deferred_revenue = nts .db.get_all(
		"Sales Invoice Item",
		filters={"parent": ["in", sales_docs], "docstatus": 1, "enable_deferred_revenue": True},
		fields=["parent"],
		as_list=1,
	)

	docs_with_deferred_expense = nts .db.get_all(
		"Purchase Invoice Item",
		filters={"parent": ["in", purchase_docs], "docstatus": 1, "enable_deferred_expense": 1},
		fields=["parent"],
		as_list=1,
	)

	if docs_with_deferred_revenue or docs_with_deferred_expense:
		nts .throw(
			_("Documents: {0} have deferred revenue/expense enabled for them. Cannot repost.").format(
				nts .bold(
					comma_and([x[0] for x in docs_with_deferred_expense + docs_with_deferred_revenue])
				)
			)
		)


def validate_docs_for_voucher_types(doc_voucher_types):
	allowed_types = get_allowed_types_from_settings()
	# Validate voucher types
	voucher_types = set(doc_voucher_types)
	if disallowed_types := voucher_types.difference(allowed_types):
		message = "are" if len(disallowed_types) > 1 else "is"
		nts .throw(
			_("{0} {1} not allowed to be reposted. Modify {2} to enable reposting.").format(
				nts .bold(comma_and(list(disallowed_types))),
				message,
				nts .bold(
					nts .utils.get_link_to_form(
						"Repost Accounting Ledger Settings", "Repost Accounting Ledger Settings"
					)
				),
			)
		)


@nts .whitelist()
@nts .validate_and_sanitize_search_inputs
def get_repost_allowed_types(doctype, txt, searchfield, start, page_len, filters):
	filters = {"allowed": True}

	if txt:
		filters.update({"document_type": ("like", f"%{txt}%")})

	if allowed_types := nts .db.get_all(
		"Repost Allowed Types", filters=filters, fields=["distinct(document_type)"], as_list=1
	):
		return allowed_types
	return []
