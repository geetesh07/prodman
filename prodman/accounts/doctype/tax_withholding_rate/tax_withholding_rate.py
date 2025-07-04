# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class TaxWithholdingRate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		cumulative_threshold: DF.Float
		from_date: DF.Date
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		single_threshold: DF.Float
		tax_withholding_rate: DF.Float
		to_date: DF.Date
	# end: auto-generated types

	pass
