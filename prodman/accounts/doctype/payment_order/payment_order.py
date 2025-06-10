# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts 
from nts  import _
from nts .model.document import Document
from nts .utils import nowdate

from prodman.accounts.party import get_party_account


class PaymentOrder(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.payment_order_reference.payment_order_reference import (
			PaymentOrderReference,
		)

		account: DF.Data | None
		amended_from: DF.Link | None
		company: DF.Link
		company_bank: DF.Link | None
		company_bank_account: DF.Link
		naming_series: DF.Literal["PMO-"]
		party: DF.Link | None
		payment_order_type: DF.Literal["", "Payment Request", "Payment Entry"]
		posting_date: DF.Date | None
		references: DF.Table[PaymentOrderReference]
	# end: auto-generated types

	def on_submit(self):
		self.update_payment_status()

	def on_cancel(self):
		self.update_payment_status(cancel=True)

	def update_payment_status(self, cancel=False):
		status = "Payment Ordered"
		if cancel:
			status = "Initiated"

		if self.payment_order_type == "Payment Request":
			ref_field = "status"
			ref_doc_field = nts .scrub(self.payment_order_type)
		else:
			ref_field = "payment_order_status"
			ref_doc_field = "reference_name"

		for d in self.references:
			nts .db.set_value(self.payment_order_type, d.get(ref_doc_field), ref_field, status)


@nts .whitelist()
@nts .validate_and_sanitize_search_inputs
def get_mop_query(doctype, txt, searchfield, start, page_len, filters):
	return nts .db.sql(
		""" select mode_of_payment from `tabPayment Order Reference`
		where parent = %(parent)s and mode_of_payment like %(txt)s
		limit %(page_len)s offset %(start)s""",
		{"parent": filters.get("parent"), "start": start, "page_len": page_len, "txt": "%%%s%%" % txt},
	)


@nts .whitelist()
@nts .validate_and_sanitize_search_inputs
def get_supplier_query(doctype, txt, searchfield, start, page_len, filters):
	return nts .db.sql(
		""" select supplier from `tabPayment Order Reference`
		where parent = %(parent)s and supplier like %(txt)s and
		(payment_reference is null or payment_reference='')
		limit %(page_len)s offset %(start)s""",
		{"parent": filters.get("parent"), "start": start, "page_len": page_len, "txt": "%%%s%%" % txt},
	)


@nts .whitelist()
def make_payment_records(name, supplier, mode_of_payment=None):
	doc = nts .get_doc("Payment Order", name)
	make_journal_entry(doc, supplier, mode_of_payment)


def make_journal_entry(doc, supplier, mode_of_payment=None):
	je = nts .new_doc("Journal Entry")
	je.payment_order = doc.name
	je.posting_date = nowdate()
	mode_of_payment_type = nts ._dict(nts .get_all("Mode of Payment", fields=["name", "type"], as_list=1))

	je.voucher_type = "Bank Entry"
	if mode_of_payment and mode_of_payment_type.get(mode_of_payment) == "Cash":
		je.voucher_type = "Cash Entry"

	paid_amt = 0
	party_account = get_party_account("Supplier", supplier, doc.company)
	for d in doc.references:
		if d.supplier == supplier and (not mode_of_payment or mode_of_payment == d.mode_of_payment):
			je.append(
				"accounts",
				{
					"account": party_account,
					"debit_in_account_currency": d.amount,
					"party_type": "Supplier",
					"party": supplier,
					"reference_type": d.reference_doctype,
					"reference_name": d.reference_name,
				},
			)

			paid_amt += d.amount

	je.append("accounts", {"account": doc.account, "credit_in_account_currency": paid_amt})

	je.flags.ignore_mandatory = True
	je.save()
	nts .msgprint(_("{0} {1} created").format(je.doctype, je.name))
