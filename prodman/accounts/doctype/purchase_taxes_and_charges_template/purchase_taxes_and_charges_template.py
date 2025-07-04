# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts 
from nts .model.document import Document

from prodman.accounts.doctype.sales_taxes_and_charges_template.sales_taxes_and_charges_template import (
	valdiate_taxes_and_charges_template,
)


class PurchaseTaxesandChargesTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.purchase_taxes_and_charges.purchase_taxes_and_charges import (
			PurchaseTaxesandCharges,
		)

		company: DF.Link
		disabled: DF.Check
		is_default: DF.Check
		tax_category: DF.Link | None
		taxes: DF.Table[PurchaseTaxesandCharges]
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		valdiate_taxes_and_charges_template(self)

	def autoname(self):
		if self.company and self.title:
			abbr = nts .get_cached_value("Company", self.company, "abbr")
			self.name = f"{self.title} - {abbr}"
