import nts


def execute():
	if nts.db.has_table("Tax Withholding Category") and nts.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		nts.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
