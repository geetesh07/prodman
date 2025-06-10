# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts

from prodman.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = nts.get_all("Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]})
	if not company:
		return

	nts.reload_doc("accounts", "doctype", "pos_invoice")
	nts.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()
