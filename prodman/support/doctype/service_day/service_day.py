# Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts
from nts.model.document import Document


class ServiceDay(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		end_time: DF.Time
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		start_time: DF.Time
		workday: DF.Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	# end: auto-generated types

	pass
