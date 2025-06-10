# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.exists("DocType", "Bank Reconciliation Detail") and nts.db.exists(
		"DocType", "Bank Clearance Detail"
	):
		nts.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
