# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts 
from nts  import _
from nts .model.document import Document


class BankGuarantee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		account: DF.Link | None
		amended_from: DF.Link | None
		amount: DF.Currency
		bank: DF.Link | None
		bank_account: DF.Link | None
		bank_account_no: DF.Data | None
		bank_guarantee_number: DF.Data | None
		bg_type: DF.Literal["", "Receiving", "Providing"]
		branch_code: DF.Data | None
		charges: DF.Currency
		customer: DF.Link | None
		end_date: DF.Date | None
		fixed_deposit_number: DF.Data | None
		iban: DF.Data | None
		margin_money: DF.Currency
		more_information: DF.TextEditor | None
		name_of_beneficiary: DF.Data | None
		project: DF.Link | None
		reference_docname: DF.DynamicLink | None
		reference_doctype: DF.Link | None
		start_date: DF.Date
		supplier: DF.Link | None
		swift_number: DF.Data | None
		validity: DF.Int
	# end: auto-generated types

	def validate(self):
		if not (self.customer or self.supplier):
			nts .throw(_("Select the customer or supplier."))

	def on_submit(self):
		if not self.bank_guarantee_number:
			nts .throw(_("Enter the Bank Guarantee Number before submittting."))
		if not self.name_of_beneficiary:
			nts .throw(_("Enter the name of the Beneficiary before submittting."))
		if not self.bank:
			nts .throw(_("Enter the name of the bank or lending institution before submittting."))


@nts .whitelist()
def get_voucher_details(bank_guarantee_type: str, reference_name: str):
	if not isinstance(reference_name, str):
		raise TypeError("reference_name must be a string")

	fields_to_fetch = ["grand_total"]

	if bank_guarantee_type == "Receiving":
		doctype = "Sales Order"
		fields_to_fetch.append("customer")
		fields_to_fetch.append("project")
	else:
		doctype = "Purchase Order"
		fields_to_fetch.append("supplier")

	return nts .db.get_value(doctype, reference_name, fields_to_fetch, as_dict=True)
