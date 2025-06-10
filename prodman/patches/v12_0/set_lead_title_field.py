import nts


def execute():
	nts.reload_doc("crm", "doctype", "lead")
	nts.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
