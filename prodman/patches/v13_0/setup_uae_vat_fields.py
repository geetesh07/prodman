# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt

import nts

from prodman.regional.united_arab_emirates.setup import setup


def execute():
	company = nts.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	nts.reload_doc("regional", "report", "uae_vat_201")
	nts.reload_doc("regional", "doctype", "uae_vat_settings")
	nts.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
