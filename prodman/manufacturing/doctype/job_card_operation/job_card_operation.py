# Copyright (c) 2020, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts
from nts.model.document import Document


class JobCardOperation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		completed_qty: DF.Float
		completed_time: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		status: DF.Literal["Complete", "Pause", "Pending", "Work In Progress"]
		sub_operation: DF.Link | None
	# end: auto-generated types

	pass
