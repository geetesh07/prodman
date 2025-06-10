# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts.model.document import Document
from nts.model.naming import set_name_by_naming_series


class Campaign(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.crm.doctype.campaign_email_schedule.campaign_email_schedule import (
			CampaignEmailSchedule,
		)

		campaign_name: DF.Data
		campaign_schedules: DF.Table[CampaignEmailSchedule]
		description: DF.Text | None
		naming_series: DF.Literal["SAL-CAM-.YYYY.-"]
	# end: auto-generated types

	def autoname(self):
		if nts.defaults.get_global_default("campaign_naming_by") != "Naming Series":
			self.name = self.campaign_name
		else:
			set_name_by_naming_series(self)
