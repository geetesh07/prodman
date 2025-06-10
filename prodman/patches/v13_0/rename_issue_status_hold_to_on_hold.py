# Copyright (c) 2020, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.exists("DocType", "Issue"):
		nts.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	nts.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
