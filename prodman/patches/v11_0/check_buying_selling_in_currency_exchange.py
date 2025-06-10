import nts


def execute():
	nts.reload_doc("setup", "doctype", "currency_exchange")
	nts.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
