# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from nts.model.document import Document


class ItemQualityInspectionParameter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		acceptance_formula: DF.Code | None
		formula_based_criteria: DF.Check
		max_value: DF.Float
		min_value: DF.Float
		numeric: DF.Check
		parameter_group: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		specification: DF.Link
		value: DF.Data | None
	# end: auto-generated types

	pass
