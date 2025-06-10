# Copyright (c) 2018, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	"""
	default supplier was not set in the item defaults for multi company instance,
	        this patch will set the default supplier

	"""
	if not nts.db.has_column("Item", "default_supplier"):
		return

	nts.reload_doc("stock", "doctype", "item_default")
	nts.reload_doc("stock", "doctype", "item")

	companies = nts.get_all("Company")
	if len(companies) > 1:
		nts.db.sql(
			""" UPDATE `tabItem Default`, `tabItem`
			SET `tabItem Default`.default_supplier = `tabItem`.default_supplier
			WHERE
				`tabItem Default`.parent = `tabItem`.name and `tabItem Default`.default_supplier is null
				and `tabItem`.default_supplier is not null and `tabItem`.default_supplier != '' """
		)
