# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.exists("Company", {"country": "India"}):
		return

	nts.reload_doc("core", "doctype", "has_role")
	nts.db.sql(
		"""
		delete from
			`tabHas Role`
		where
			parenttype = 'Report' and parent in('GST Sales Register',
				'GST Purchase Register', 'GST Itemised Sales Register',
				'GST Itemised Purchase Register', 'Eway Bill')
		"""
	)
