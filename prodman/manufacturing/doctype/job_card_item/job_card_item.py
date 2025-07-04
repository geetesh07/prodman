# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class JobCardItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		allow_alternative_item: DF.Check
		description: DF.Text | None
		item_code: DF.Link | None
		item_group: DF.Link | None
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		required_qty: DF.Float
		source_warehouse: DF.Link | None
		stock_uom: DF.Link | None
		transferred_qty: DF.Float
		uom: DF.Link | None
	# end: auto-generated types

	pass
