# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


from nts.model.document import Document


class OpportunityItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		amount: DF.Currency
		base_amount: DF.Currency
		base_rate: DF.Currency
		brand: DF.Link | None
		description: DF.TextEditor | None
		image: DF.Attach | None
		item_code: DF.Link | None
		item_group: DF.Link | None
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		rate: DF.Currency
		uom: DF.Link | None
	# end: auto-generated types

	pass
