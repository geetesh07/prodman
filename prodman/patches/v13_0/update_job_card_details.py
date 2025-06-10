# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("manufacturing", "doctype", "job_card")
	nts.reload_doc("manufacturing", "doctype", "job_card_item")
	nts.reload_doc("manufacturing", "doctype", "work_order_operation")

	nts.db.sql(
		""" update `tabJob Card` jc, `tabWork Order Operation` wo
		SET	jc.hour_rate =  wo.hour_rate
		WHERE
			jc.operation_id = wo.name and jc.docstatus < 2 and wo.hour_rate > 0
	"""
	)
