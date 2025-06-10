import nts


def execute():
	nts.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	nts.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	nts.reload_doc("accounts", "doctype", "bank_account")
