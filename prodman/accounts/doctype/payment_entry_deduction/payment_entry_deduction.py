# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class PaymentEntryDeduction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		account: DF.Link
		amount: DF.Currency
		cost_center: DF.Link
		description: DF.SmallText | None
		is_exchange_gain_loss: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
