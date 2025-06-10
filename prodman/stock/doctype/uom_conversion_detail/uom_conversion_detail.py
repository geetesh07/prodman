# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from nts.model.document import Document


class UOMConversionDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		conversion_factor: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		uom: DF.Link | None
	# end: auto-generated types

	pass
