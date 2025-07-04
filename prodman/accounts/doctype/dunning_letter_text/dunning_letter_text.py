# Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts 
from nts .model.document import Document


class DunningLetterText(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		body_text: DF.TextEditor | None
		closing_text: DF.TextEditor | None
		is_default_language: DF.Check
		language: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
