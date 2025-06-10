import nts


def execute():
	nts.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		nts.db.table_exists("Bank")
		and nts.db.table_exists("Bank Account")
		and nts.db.has_column("Bank Account", "swift_number")
	):
		try:
			nts.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception:
			nts.log_error("Bank to Bank Account patch migration failed")

	nts.reload_doc("accounts", "doctype", "bank_account")
	nts.reload_doc("accounts", "doctype", "payment_request")
