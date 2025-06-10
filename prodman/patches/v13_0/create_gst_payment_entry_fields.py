# Copyright (c) 2021, nts and Contributors
# License: GNU General Public License v3. See license.txt

import nts


# Patch kept for users outside India
def execute():
	if nts.db.exists("Company", {"country": "India"}):
		return

	for field in (
		"gst_section",
		"company_address",
		"company_gstin",
		"place_of_supply",
		"customer_address",
		"customer_gstin",
	):
		nts.delete_doc_if_exists("Custom Field", f"Payment Entry-{field}")
