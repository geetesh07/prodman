# Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts
from nts.model.document import Document


class PickListItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		batch_no: DF.Link | None
		conversion_factor: DF.Float
		description: DF.Text | None
		item_code: DF.Link
		item_group: DF.Data | None
		item_name: DF.Data | None
		material_request: DF.Link | None
		material_request_item: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		picked_qty: DF.Float
		product_bundle_item: DF.Data | None
		qty: DF.Float
		sales_order: DF.Link | None
		sales_order_item: DF.Data | None
		serial_and_batch_bundle: DF.Link | None
		serial_no: DF.SmallText | None
		stock_qty: DF.Float
		stock_reserved_qty: DF.Float
		stock_uom: DF.Link | None
		uom: DF.Link | None
		use_serial_batch_fields: DF.Check
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
