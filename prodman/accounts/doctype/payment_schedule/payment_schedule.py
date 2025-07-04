# Copyright (c) 2017, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class PaymentSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		base_outstanding: DF.Currency
		base_paid_amount: DF.Currency
		base_payment_amount: DF.Currency
		description: DF.SmallText | None
		discount: DF.Float
		discount_date: DF.Date | None
		discount_type: DF.Literal["Percentage", "Amount"]
		discounted_amount: DF.Currency
		due_date: DF.Date
		invoice_portion: DF.Percent
		mode_of_payment: DF.Link | None
		outstanding: DF.Currency
		paid_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		payment_amount: DF.Currency
		payment_term: DF.Link | None
	# end: auto-generated types

	pass
