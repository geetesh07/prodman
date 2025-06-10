import nts


def execute():
	if nts.db.exists("DocType", "Membership"):
		if "webhook_payload" in nts.db.get_table_columns("Membership"):
			nts.db.sql("alter table `tabMembership` drop column webhook_payload")
