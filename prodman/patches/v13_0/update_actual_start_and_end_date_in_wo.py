# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.utils import add_to_date


def execute():
	nts.reload_doc("manufacturing", "doctype", "work_order")
	nts.reload_doc("manufacturing", "doctype", "work_order_item")
	nts.reload_doc("manufacturing", "doctype", "job_card")

	data = nts.get_all(
		"Work Order", filters={"docstatus": 1, "status": ("in", ["In Process", "Completed"])}
	)

	for d in data:
		doc = nts.get_doc("Work Order", d.name)
		doc.set_actual_dates()
		doc.db_set("actual_start_date", doc.actual_start_date, update_modified=False)

		if doc.status == "Completed":
			nts.db.set_value(
				"Work Order",
				d.name,
				{"actual_end_date": doc.actual_end_date, "lead_time": doc.lead_time},
				update_modified=False,
			)

			if not doc.planned_end_date:
				add_to_date(doc.planned_start_date, minutes=doc.lead_time)
				doc.db_set("planned_end_date", doc.actual_start_date, update_modified=False)

	nts.db.sql(
		""" UPDATE `tabJob Card` as jc, `tabWork Order` as wo
		SET
			jc.production_item = wo.production_item, jc.item_name = wo.item_name
		WHERE
			jc.work_order = wo.name and IFNULL(jc.production_item, "") = ""
	"""
	)
