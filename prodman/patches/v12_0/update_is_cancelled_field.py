import nts


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not nts.db.has_column(doctype, "is_cancelled")
			or nts.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		nts.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL"""
		)
		nts.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'"""
		)

		nts.reload_doc(module, "doctype", nts.scrub(doctype))
