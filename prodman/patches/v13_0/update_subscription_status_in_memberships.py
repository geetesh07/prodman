import nts


def execute():
	if nts.db.exists("DocType", "Member"):
		nts.reload_doc("Non Profit", "doctype", "Member")

		if nts.db.has_column("Member", "subscription_activated"):
			nts.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			nts.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
