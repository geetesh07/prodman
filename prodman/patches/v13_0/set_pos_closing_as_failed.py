import nts


def execute():
	nts.reload_doc("accounts", "doctype", "pos_closing_entry")

	nts.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
