import nts


def execute():
	nts.reload_doc("manufacturing", "doctype", "workstation")

	nts.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
