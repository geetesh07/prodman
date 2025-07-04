# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.utils import cint, flt


class Routing(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.manufacturing.doctype.bom_operation.bom_operation import BOMOperation

		disabled: DF.Check
		operations: DF.Table[BOMOperation]
		routing_name: DF.Data | None
	# end: auto-generated types

	def validate(self):
		self.calculate_operating_cost()
		self.set_routing_id()

	def on_update(self):
		self.calculate_operating_cost()

	def calculate_operating_cost(self):
		for operation in self.operations:
			if not operation.hour_rate:
				operation.hour_rate = nts.db.get_value("Workstation", operation.workstation, "hour_rate")
			operation.operating_cost = flt(
				flt(operation.hour_rate) * flt(operation.time_in_mins) / 60,
				operation.precision("operating_cost"),
			)

	def set_routing_id(self):
		sequence_id = 0
		for row in self.operations:
			if not row.sequence_id:
				row.sequence_id = sequence_id + 1
			elif sequence_id and row.sequence_id and cint(sequence_id) > cint(row.sequence_id):
				nts.throw(
					_(
						"At row #{0}: the sequence id {1} cannot be less than previous row sequence id {2}"
					).format(row.idx, row.sequence_id, sequence_id)
				)

			sequence_id = row.sequence_id
