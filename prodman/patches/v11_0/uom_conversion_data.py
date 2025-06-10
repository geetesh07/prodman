import nts


def execute():
	from prodman.setup.setup_wizard.operations.install_fixtures import add_uom_data

	nts.reload_doc("setup", "doctype", "UOM Conversion Factor")
	nts.reload_doc("setup", "doctype", "UOM")
	nts.reload_doc("stock", "doctype", "UOM Category")

	if not nts.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		nts.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			nts.delete_doc("UOM", "Hundredweight")
			nts.delete_doc("UOM", "Pound Cubic Yard")
		except nts.LinkExistsError:
			pass

		add_uom_data()
