# Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts 
from nts .model.document import Document


class AllowedDimension(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		accounting_dimension: DF.Link | None
		dimension_value: DF.DynamicLink | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
