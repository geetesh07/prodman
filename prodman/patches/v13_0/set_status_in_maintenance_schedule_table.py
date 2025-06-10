import nts


def execute():
	nts.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	nts.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
