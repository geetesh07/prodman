import nts


def execute():
	nts.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	nts.cache().delete_key("home_settings")
