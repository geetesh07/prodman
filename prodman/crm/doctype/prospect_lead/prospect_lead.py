# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import nts
from nts.model.document import Document


class ProspectLead(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		email: DF.Data | None
		lead: DF.Link
		lead_name: DF.Data | None
		lead_owner: DF.Data | None
		mobile_no: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		status: DF.Data | None
	# end: auto-generated types

	pass
