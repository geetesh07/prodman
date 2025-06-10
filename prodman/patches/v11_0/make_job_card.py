# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts

from prodman.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	nts.reload_doc("manufacturing", "doctype", "work_order")
	nts.reload_doc("manufacturing", "doctype", "work_order_item")
	nts.reload_doc("manufacturing", "doctype", "job_card")
	nts.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = nts.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = nts.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in nts.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = nts.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			nts.delete_doc("Timesheet", d.name)
