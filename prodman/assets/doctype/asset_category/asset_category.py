# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts 
from nts  import _
from nts .model.document import Document
from nts .utils import cint, get_link_to_form


class AssetCategory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.assets.doctype.asset_category_account.asset_category_account import AssetCategoryAccount
		from prodman.assets.doctype.asset_finance_book.asset_finance_book import AssetFinanceBook

		accounts: DF.Table[AssetCategoryAccount]
		asset_category_name: DF.Data
		enable_cwip_accounting: DF.Check
		finance_books: DF.Table[AssetFinanceBook]
		non_depreciable_category: DF.Check
	# end: auto-generated types

	def validate(self):
		self.validate_finance_books()
		self.validate_account_types()
		self.validate_account_currency()
		self.valide_cwip_account()

	def validate_finance_books(self):
		for d in self.finance_books:
			for field in ("Total Number of Depreciations", "Frequency of Depreciation"):
				if cint(d.get(nts .scrub(field))) < 1:
					nts .throw(
						_("Row {0}: {1} must be greater than 0").format(d.idx, field), nts .MandatoryError
					)

	def validate_account_currency(self):
		account_types = [
			"fixed_asset_account",
			"accumulated_depreciation_account",
			"depreciation_expense_account",
			"capital_work_in_progress_account",
		]
		invalid_accounts = []
		for d in self.accounts:
			company_currency = nts .get_value("Company", d.get("company_name"), "default_currency")
			for type_of_account in account_types:
				if d.get(type_of_account):
					account_currency = nts .get_value("Account", d.get(type_of_account), "account_currency")
					if account_currency != company_currency:
						invalid_accounts.append(
							nts ._dict(
								{"type": type_of_account, "idx": d.idx, "account": d.get(type_of_account)}
							)
						)

		for d in invalid_accounts:
			nts .throw(
				_("Row #{}: Currency of {} - {} doesn't matches company currency.").format(
					d.idx, nts .bold(nts .unscrub(d.type)), nts .bold(d.account)
				),
				title=_("Invalid Account"),
			)

	def validate_account_types(self):
		account_type_map = {
			"fixed_asset_account": {"account_type": ["Fixed Asset"]},
			"accumulated_depreciation_account": {"account_type": ["Accumulated Depreciation"]},
			"depreciation_expense_account": {"account_type": ["Depreciation"]},
			"capital_work_in_progress_account": {"account_type": ["Capital Work in Progress"]},
		}
		for d in self.accounts:
			for fieldname in account_type_map.keys():
				if d.get(fieldname):
					selected_account = d.get(fieldname)
					key_to_match = next(iter(account_type_map.get(fieldname)))  # acount_type or root_type
					selected_key_type = nts .db.get_value("Account", selected_account, key_to_match)
					expected_key_types = account_type_map[fieldname][key_to_match]

					if selected_key_type not in expected_key_types:
						nts .throw(
							_(
								"Row #{0}: {1} of {2} should be {3}. Please update the {1} or select a different account."
							).format(
								d.idx,
								nts .unscrub(key_to_match),
								nts .bold(selected_account),
								nts .bold(" or ".join(expected_key_types)),
							),
							title=_("Invalid Account"),
						)

	def valide_cwip_account(self):
		if self.enable_cwip_accounting:
			missing_cwip_accounts_for_company = []
			for d in self.accounts:
				if not d.capital_work_in_progress_account and not nts .db.get_value(
					"Company", d.company_name, "capital_work_in_progress_account"
				):
					missing_cwip_accounts_for_company.append(get_link_to_form("Company", d.company_name))

			if missing_cwip_accounts_for_company:
				msg = _("""To enable Capital Work in Progress Accounting,""") + " "
				msg += _("""you must select Capital Work in Progress Account in accounts table""")
				msg += "<br><br>"
				msg += _("You can also set default CWIP account in Company {}").format(
					", ".join(missing_cwip_accounts_for_company)
				)
				nts .throw(msg, title=_("Missing Account"))


def get_asset_category_account(
	fieldname, item=None, asset=None, account=None, asset_category=None, company=None
):
	if item and nts .db.get_value("Item", item, "is_fixed_asset"):
		asset_category = nts .db.get_value("Item", item, ["asset_category"])

	elif not asset_category or not company:
		if account:
			if nts .db.get_value("Account", account, "account_type") != "Fixed Asset":
				account = None

		if not account:
			asset_details = nts .db.get_value("Asset", asset, ["asset_category", "company"])
			asset_category, company = asset_details or [None, None]

	account = nts .db.get_value(
		"Asset Category Account",
		filters={"parent": asset_category, "company_name": company},
		fieldname=fieldname,
	)

	return account
