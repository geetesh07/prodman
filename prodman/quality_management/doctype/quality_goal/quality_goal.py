# Copyright (c) 2018, nts and contributors
# For license information, please see license.txt


from nts.model.document import Document


class QualityGoal(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.quality_management.doctype.quality_goal_objective.quality_goal_objective import (
			QualityGoalObjective,
		)

		date: DF.Literal[
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			"10",
			"11",
			"12",
			"13",
			"14",
			"15",
			"16",
			"17",
			"18",
			"19",
			"20",
			"21",
			"22",
			"23",
			"24",
			"25",
			"26",
			"27",
			"28",
			"29",
			"30",
		]
		frequency: DF.Literal["None", "Daily", "Weekly", "Monthly", "Quarterly"]
		goal: DF.Data
		objectives: DF.Table[QualityGoalObjective]
		procedure: DF.Link | None
		weekday: DF.Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	# end: auto-generated types

	def validate(self):
		pass
