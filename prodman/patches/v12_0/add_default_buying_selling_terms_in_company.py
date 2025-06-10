# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("setup", "doctype", "company")
	if nts.db.has_column("Company", "default_terms"):
		rename_field("Company", "default_terms", "default_selling_terms")

		for company in nts.get_all("Company", ["name", "default_selling_terms", "default_buying_terms"]):
			if company.default_selling_terms and not company.default_buying_terms:
				nts.db.set_value(
					"Company", company.name, "default_buying_terms", company.default_selling_terms
				)

	nts.reload_doc("setup", "doctype", "terms_and_conditions")
	nts.db.sql("update `tabTerms and Conditions` set selling=1, buying=1, hr=1")
