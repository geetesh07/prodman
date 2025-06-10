# Copyright (c) 2017, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class SupplierScorecardScoringCriteria(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		criteria_name: DF.Link
		formula: DF.SmallText | None
		max_score: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		score: DF.Percent
		weight: DF.Percent
	# end: auto-generated types

	pass
