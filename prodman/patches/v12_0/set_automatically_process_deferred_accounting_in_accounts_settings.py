import nts


def execute():
	nts.reload_doc("accounts", "doctype", "accounts_settings")

	nts.db.set_single_value("Accounts Settings", "automatically_process_deferred_accounting_entry", 1)
