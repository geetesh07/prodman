# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts import _
from nts.model.document import Document


class PartySpecificItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		based_on_value: DF.DynamicLink
		party: DF.DynamicLink
		party_type: DF.Literal["Customer", "Supplier"]
		restrict_based_on: DF.Literal["Item", "Item Group", "Brand"]
	# end: auto-generated types

	def validate(self):
		exists = nts.db.exists(
			{
				"doctype": "Party Specific Item",
				"party_type": self.party_type,
				"party": self.party,
				"restrict_based_on": self.restrict_based_on,
				"based_on": self.based_on_value,
			}
		)
		if exists:
			nts.throw(_("This item filter has already been applied for the {0}").format(self.party_type))
