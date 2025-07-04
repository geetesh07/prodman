# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class BlanketOrderItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		item_code: DF.Link
		item_name: DF.Data | None
		ordered_qty: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		party_item_code: DF.Data | None
		qty: DF.Float
		rate: DF.Currency
		terms_and_conditions: DF.Text | None
	# end: auto-generated types

	pass
