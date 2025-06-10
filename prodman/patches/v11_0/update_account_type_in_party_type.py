# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("setup", "doctype", "party_type")
	party_types = {
		"Customer": "Receivable",
		"Supplier": "Payable",
		"Employee": "Payable",
		"Member": "Receivable",
		"Shareholder": "Payable",
	}

	for party_type, account_type in party_types.items():
		nts.db.set_value("Party Type", party_type, "account_type", account_type)
