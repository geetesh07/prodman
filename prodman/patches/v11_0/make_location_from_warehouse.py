# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.utils.nestedset import rebuild_tree


def execute():
	if not nts.db.get_value("Asset", {"docstatus": ("<", 2)}, "name"):
		return
	nts.reload_doc("assets", "doctype", "location")
	nts.reload_doc("stock", "doctype", "warehouse")

	for d in nts.get_all(
		"Warehouse", fields=["warehouse_name", "is_group", "parent_warehouse"], order_by="lft asc"
	):
		try:
			loc = nts.new_doc("Location")
			loc.location_name = d.warehouse_name
			loc.is_group = d.is_group
			loc.flags.ignore_mandatory = True
			if d.parent_warehouse:
				loc.parent_location = get_parent_warehouse_name(d.parent_warehouse)

			loc.save(ignore_permissions=True)
		except nts.DuplicateEntryError:
			continue

	rebuild_tree("Location", "parent_location")


def get_parent_warehouse_name(warehouse):
	return nts.db.get_value("Warehouse", warehouse, "warehouse_name")
