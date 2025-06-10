# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.db.sql(
		"""
		DELETE FROM `tabProperty Setter`
		WHERE doc_type in ('Sales Invoice', 'Purchase Invoice', 'Payment Entry')
		AND field_name = 'cost_center'
		AND property = 'hidden'
	"""
	)
