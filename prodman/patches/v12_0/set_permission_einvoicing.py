import nts
from nts.permissions import add_permission, update_permission_property

from prodman.regional.italy.setup import make_custom_fields


def execute():
	company = nts.get_all("Company", filters={"country": "Italy"})

	if not company:
		return

	make_custom_fields()

	nts.reload_doc("regional", "doctype", "import_supplier_invoice")

	add_permission("Import Supplier Invoice", "Accounts Manager", 0)
	update_permission_property("Import Supplier Invoice", "Accounts Manager", 0, "write", 1)
	update_permission_property("Import Supplier Invoice", "Accounts Manager", 0, "create", 1)
