# Copyright (c) 2020, nts and Contributors
# License: GNU General Public License v3. See license.txt

import nts


def _rename_single_field(**kwargs):
	count = nts.db.sql(
		"SELECT COUNT(*) FROM tabSingles WHERE doctype='{doctype}' AND field='{new_name}';".format(**kwargs)
	)[0][0]  # nosec
	if count == 0:
		nts.db.sql(
			"UPDATE tabSingles SET field='{new_name}' WHERE doctype='{doctype}' AND field='{old_name}';".format(
				**kwargs
			)
		)  # nosec


def execute():
	_rename_single_field(doctype="Bank Clearance", old_name="bank_account", new_name="account")
	_rename_single_field(doctype="Bank Clearance", old_name="bank_account_no", new_name="bank_account")
	nts.reload_doc("Accounts", "doctype", "Bank Clearance")
