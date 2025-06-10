# Copyright (c) 2017, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document


class ProjectType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		description: DF.Text | None
		project_type: DF.Data
	# end: auto-generated types

	def on_trash(self):
		if self.name == "External":
			nts.throw(_("You cannot delete Project Type 'External'"))
