# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


from nts .model.document import Document


class PaymentReconciliationInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		amount: DF.Currency
		currency: DF.Link | None
		exchange_rate: DF.Float
		invoice_date: DF.Date | None
		invoice_number: DF.DynamicLink | None
		invoice_type: DF.Literal["Sales Invoice", "Purchase Invoice", "Journal Entry"]
		outstanding_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	@staticmethod
	def get_list(args):
		pass
