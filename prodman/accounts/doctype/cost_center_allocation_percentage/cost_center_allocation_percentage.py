# Copyright (c) 2022, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import nts 
from nts .model.document import Document


class CostCenterAllocationPercentage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		cost_center: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Percent
	# end: auto-generated types

	pass
