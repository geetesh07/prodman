# Copyright (c) 2017, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class AssetMaintenanceTeam(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.assets.doctype.maintenance_team_member.maintenance_team_member import (
			MaintenanceTeamMember,
		)

		company: DF.Link
		maintenance_manager: DF.Link | None
		maintenance_manager_name: DF.ReadOnly | None
		maintenance_team_members: DF.Table[MaintenanceTeamMember]
		maintenance_team_name: DF.Data
	# end: auto-generated types

	pass
