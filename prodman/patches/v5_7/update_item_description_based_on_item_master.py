import nts


def execute():
	name = nts.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:nts.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		nts.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
