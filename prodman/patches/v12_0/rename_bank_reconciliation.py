# Copyright (c) 2018, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.table_exists("Bank Reconciliation"):
		nts.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		nts.reload_doc("Accounts", "doctype", "Bank Clearance")

		nts.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		nts.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
