import nts


def execute():
	# nosemgrep
	nts.db.sql(
		"""
		DELETE FROM `tabAsset Movement Item`
		WHERE parent NOT IN (SELECT name FROM `tabAsset Movement`)
		"""
	)
