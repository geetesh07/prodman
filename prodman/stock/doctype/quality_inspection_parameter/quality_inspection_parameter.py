# Copyright (c) 2020, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts
from nts.model.document import Document


class QualityInspectionParameter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		description: DF.TextEditor | None
		parameter: DF.Data
		parameter_group: DF.Link | None
	# end: auto-generated types

	pass
