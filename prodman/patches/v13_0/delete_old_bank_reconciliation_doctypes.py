# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	doctypes = [
		"Bank Statement Settings",
		"Bank Statement Settings Item",
		"Bank Statement Transaction Entry",
		"Bank Statement Transaction Invoice Item",
		"Bank Statement Transaction Payment Item",
		"Bank Statement Transaction Settings Item",
		"Bank Statement Transaction Settings",
	]

	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, force=1)

	nts.delete_doc("Page", "bank-reconciliation", force=1)

	nts.reload_doc("accounts", "doctype", "bank_transaction")

	rename_field("Bank Transaction", "debit", "deposit")
	rename_field("Bank Transaction", "credit", "withdrawal")
