# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json

import nts
from nts import _, throw
from nts.model.document import Document
from nts.utils import cint
from nts.utils.jinja import validate_template


class TermsandConditions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		buying: DF.Check
		disabled: DF.Check
		selling: DF.Check
		terms: DF.TextEditor | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if not cint(self.buying) and not cint(self.selling) and not cint(self.hr) and not cint(self.disabled):
			throw(_("At least one of the Applicable Modules should be selected"))


@nts.whitelist()
def get_terms_and_conditions(template_name, doc):
	if isinstance(doc, str):
		doc = json.loads(doc)

	terms_and_conditions = nts.get_doc("Terms and Conditions", template_name)

	if terms_and_conditions.terms:
		return nts.render_template(terms_and_conditions.terms, doc)
