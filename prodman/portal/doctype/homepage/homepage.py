# Copyright (c) 2015, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts.model.document import Document
from nts.website.utils import delete_page_cache


class Homepage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		company: DF.Link
		description: DF.Text
		hero_image: DF.AttachImage | None
		hero_section: DF.Link | None
		hero_section_based_on: DF.Literal["Default", "Slideshow", "Homepage Section"]
		slideshow: DF.Link | None
		tag_line: DF.Data
		title: DF.Data | None
	# end: auto-generated types

	def validate(self):
		if not self.description:
			self.description = nts._("This is an example website auto-generated from prodman")
		delete_page_cache("home")
