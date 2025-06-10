# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("accounts", "doctype", "subscription")
	nts.reload_doc("accounts", "doctype", "subscription_invoice")
	nts.reload_doc("accounts", "doctype", "subscription_plan")

	if nts.db.has_column("Subscription", "customer"):
		nts.db.sql(
			"""
			UPDATE `tabSubscription`
			SET
				start_date = start,
				party_type = 'Customer',
				party = customer,
				sales_tax_template = tax_template
			WHERE IFNULL(party,'') = ''
		"""
		)

	nts.db.sql(
		"""
		UPDATE `tabSubscription Invoice`
		SET document_type = 'Sales Invoice'
		WHERE IFNULL(document_type, '') = ''
	"""
	)

	price_determination_map = {
		"Fixed rate": "Fixed Rate",
		"Based on price list": "Based On Price List",
	}

	for key, value in price_determination_map.items():
		nts.db.sql(
			"""
			UPDATE `tabSubscription Plan`
			SET price_determination = %s
			WHERE price_determination = %s
		""",
			(value, key),
		)
