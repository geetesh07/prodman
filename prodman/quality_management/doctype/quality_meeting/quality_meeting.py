# Copyright (c) 2018, nts and contributors
# For license information, please see license.txt


from nts.model.document import Document


class QualityMeeting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.quality_management.doctype.quality_meeting_agenda.quality_meeting_agenda import (
			QualityMeetingAgenda,
		)
		from prodman.quality_management.doctype.quality_meeting_minutes.quality_meeting_minutes import (
			QualityMeetingMinutes,
		)

		agenda: DF.Table[QualityMeetingAgenda]
		minutes: DF.Table[QualityMeetingMinutes]
		status: DF.Literal["Open", "Closed"]
	# end: auto-generated types

	pass
