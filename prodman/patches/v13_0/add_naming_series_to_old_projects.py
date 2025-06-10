import nts


def execute():
	nts.reload_doc("projects", "doctype", "project")

	nts.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
