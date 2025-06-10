import nts


def execute():
	company = nts.get_all("Company", filters={"country": "India"})
	if not company:
		return

	nts.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = nts.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = nts.qb.DocType("Supplier")

	nts.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
