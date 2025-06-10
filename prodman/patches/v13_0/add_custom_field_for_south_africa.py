# Copyright (c) 2020, nts and Contributors
# License: GNU General Public License v3. See license.txt

import nts

from prodman.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = nts.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	nts.reload_doc("regional", "doctype", "south_africa_vat_settings")
	nts.reload_doc("regional", "report", "vat_audit_report")
	nts.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
