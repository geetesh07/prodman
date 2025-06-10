import nts


def execute():
	from prodman.setup.setup_wizard.operations.install_fixtures import add_uom_data

	nts.reload_doc("setup", "doctype", "UOM Conversion Factor")
	nts.reload_doc("setup", "doctype", "UOM")
	nts.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
