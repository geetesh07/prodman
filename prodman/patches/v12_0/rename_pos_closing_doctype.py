# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.table_exists("POS Closing Voucher"):
		if not nts.db.exists("DocType", "POS Closing Entry"):
			nts.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not nts.db.exists("DocType", "POS Closing Entry Taxes"):
			nts.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not nts.db.exists("DocType", "POS Closing Voucher Details"):
			nts.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		nts.reload_doc("Accounts", "doctype", "POS Closing Entry")
		nts.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		nts.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if nts.db.exists("DocType", "POS Closing Voucher"):
		nts.delete_doc("DocType", "POS Closing Voucher")
		nts.delete_doc("DocType", "POS Closing Voucher Taxes")
		nts.delete_doc("DocType", "POS Closing Voucher Details")
		nts.delete_doc("DocType", "POS Closing Voucher Invoices")
