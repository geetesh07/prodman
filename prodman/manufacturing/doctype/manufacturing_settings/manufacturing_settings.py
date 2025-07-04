# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


import nts
from dateutil.relativedelta import relativedelta
from nts.model.document import Document
from nts.utils import cint


class ManufacturingSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		add_corrective_operation_cost_in_finished_good_valuation: DF.Check
		allow_overtime: DF.Check
		allow_production_on_holidays: DF.Check
		backflush_raw_materials_based_on: DF.Literal["BOM", "Material Transferred for Manufacture"]
		capacity_planning_for_days: DF.Int
		default_fg_warehouse: DF.Link | None
		default_scrap_warehouse: DF.Link | None
		default_wip_warehouse: DF.Link | None
		disable_capacity_planning: DF.Check
		enforce_time_logs: DF.Check
		get_rm_cost_from_consumption_entry: DF.Check
		job_card_excess_transfer: DF.Check
		make_serial_no_batch_from_work_order: DF.Check
		material_consumption: DF.Check
		mins_between_operations: DF.Int
		overproduction_percentage_for_sales_order: DF.Percent
		overproduction_percentage_for_work_order: DF.Percent
		set_op_cost_and_scrap_from_sub_assemblies: DF.Check
		update_bom_costs_automatically: DF.Check
		validate_components_quantities_per_bom: DF.Check
	# end: auto-generated types

	def before_save(self):
		self.reset_values()

	def reset_values(self):
		if self.backflush_raw_materials_based_on != "BOM" and self.validate_components_quantities_per_bom:
			self.validate_components_quantities_per_bom = 0


def get_mins_between_operations():
	return relativedelta(
		minutes=cint(nts.db.get_single_value("Manufacturing Settings", "mins_between_operations")) or 10
	)


@nts.whitelist()
def is_material_consumption_enabled():
	if not hasattr(nts.local, "material_consumption"):
		nts.local.material_consumption = cint(
			nts.db.get_single_value("Manufacturing Settings", "material_consumption")
		)

	return nts.local.material_consumption
