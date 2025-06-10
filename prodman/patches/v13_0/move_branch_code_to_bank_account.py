# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("accounts", "doctype", "bank_account")
	nts.reload_doc("accounts", "doctype", "bank")

	if nts.db.has_column("Bank", "branch_code") and nts.db.has_column("Bank Account", "branch_code"):
		nts.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
