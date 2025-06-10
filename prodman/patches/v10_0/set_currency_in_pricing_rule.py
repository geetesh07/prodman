import nts


def execute():
	nts.reload_doctype("Pricing Rule")

	currency = nts.db.get_default("currency")
	for doc in nts.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = nts.get_cached_value("Company", doc.company, "default_currency")

		nts.db.sql("""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name))
