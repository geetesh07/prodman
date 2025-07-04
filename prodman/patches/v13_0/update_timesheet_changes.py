import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("projects", "doctype", "timesheet")
	nts.reload_doc("projects", "doctype", "timesheet_detail")

	if nts.db.has_column("Timesheet Detail", "billable"):
		rename_field("Timesheet Detail", "billable", "is_billable")

	base_currency = nts.defaults.get_global_default("currency")

	nts.db.sql(
		"""UPDATE `tabTimesheet Detail`
			SET base_billing_rate = billing_rate,
			base_billing_amount = billing_amount,
			base_costing_rate = costing_rate,
			base_costing_amount = costing_amount"""
	)

	nts.db.sql(
		f"""UPDATE `tabTimesheet`
			SET currency = '{base_currency}',
			exchange_rate = 1.0,
			base_total_billable_amount = total_billable_amount,
			base_total_billed_amount = total_billed_amount,
			base_total_costing_amount = total_costing_amount"""
	)
