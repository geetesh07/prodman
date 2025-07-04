# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


from nts.model.document import Document


class ItemReorder(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		material_request_type: DF.Literal["Purchase", "Transfer", "Material Issue", "Manufacture"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		warehouse: DF.Link
		warehouse_group: DF.Link | None
		warehouse_reorder_level: DF.Float
		warehouse_reorder_qty: DF.Float
	# end: auto-generated types

	pass
