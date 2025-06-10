# Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts
from nts.model.document import Document


class QualityGoalObjective(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		objective: DF.Text
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		target: DF.Data | None
		uom: DF.Link | None
	# end: auto-generated types

	pass
