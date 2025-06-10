# Copyright (c) 2021, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts 
from nts  import _, bold
from nts .model.document import Document


class PartyLink(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		primary_party: DF.DynamicLink | None
		primary_role: DF.Link
		secondary_party: DF.DynamicLink | None
		secondary_role: DF.Link | None
	# end: auto-generated types

	def validate(self):
		if self.primary_role not in ["Customer", "Supplier"]:
			nts .throw(
				_(
					"Allowed primary roles are 'Customer' and 'Supplier'. Please select one of these roles only."
				),
				title=_("Invalid Primary Role"),
			)

		existing_party_link = nts .get_all(
			"Party Link",
			{"primary_party": self.primary_party, "secondary_party": self.secondary_party},
			pluck="primary_role",
		)
		if existing_party_link:
			nts .throw(
				_("{} {} is already linked with {} {}").format(
					self.primary_role,
					bold(self.primary_party),
					self.secondary_role,
					bold(self.secondary_party),
				)
			)

		existing_party_link = nts .get_all(
			"Party Link", {"primary_party": self.secondary_party}, pluck="primary_role"
		)
		if existing_party_link:
			nts .throw(
				_("{} {} is already linked with another {}").format(
					self.secondary_role, self.secondary_party, existing_party_link[0]
				)
			)

		existing_party_link = nts .get_all(
			"Party Link", {"secondary_party": self.primary_party}, pluck="primary_role"
		)
		if existing_party_link:
			nts .throw(
				_("{} {} is already linked with another {}").format(
					self.primary_role, self.primary_party, existing_party_link[0]
				)
			)


@nts .whitelist()
def create_party_link(primary_role, primary_party, secondary_party):
	party_link = nts .new_doc("Party Link")
	party_link.primary_role = primary_role
	party_link.primary_party = primary_party
	party_link.secondary_role = "Customer" if primary_role == "Supplier" else "Supplier"
	party_link.secondary_party = secondary_party

	party_link.save(ignore_permissions=True)

	return party_link
