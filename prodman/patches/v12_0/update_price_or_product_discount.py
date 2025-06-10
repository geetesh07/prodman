import nts


def execute():
	nts.reload_doc("accounts", "doctype", "pricing_rule")

	nts.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
