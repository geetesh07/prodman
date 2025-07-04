# Copyright (c) 2017, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class DepreciationSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		accumulated_depreciation_amount: DF.Currency
		depreciation_amount: DF.Currency
		journal_entry: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		schedule_date: DF.Date
		shift: DF.Link | None
	# end: auto-generated types

	pass
