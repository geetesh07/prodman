# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from nts.model.document import Document


class ItemSupplier(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		supplier: DF.Link
		supplier_part_no: DF.Data | None
	# end: auto-generated types

	pass
