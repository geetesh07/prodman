# Copyright (c) 2018, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	# Rename and reload the Land Unit and Linked Land Unit doctypes
	if nts.db.table_exists("Land Unit") and not nts.db.table_exists("Location"):
		nts.rename_doc("DocType", "Land Unit", "Location", force=True)

	nts.reload_doc("assets", "doctype", "location")

	if nts.db.table_exists("Linked Land Unit") and not nts.db.table_exists("Linked Location"):
		nts.rename_doc("DocType", "Linked Land Unit", "Linked Location", force=True)

	nts.reload_doc("assets", "doctype", "linked_location")

	if not nts.db.table_exists("Crop Cycle"):
		nts.reload_doc("agriculture", "doctype", "crop_cycle")

	# Rename the fields in related doctypes
	if "linked_land_unit" in nts.db.get_table_columns("Crop Cycle"):
		rename_field("Crop Cycle", "linked_land_unit", "linked_location")

	if "land_unit" in nts.db.get_table_columns("Linked Location"):
		rename_field("Linked Location", "land_unit", "location")

	if not nts.db.exists("Location", "All Land Units"):
		nts.get_doc({"doctype": "Location", "is_group": True, "location_name": "All Land Units"}).insert(
			ignore_permissions=True
		)

	if nts.db.table_exists("Land Unit"):
		land_units = nts.get_all("Land Unit", fields=["*"], order_by="lft")

		for land_unit in land_units:
			if not nts.db.exists("Location", land_unit.get("land_unit_name")):
				nts.get_doc(
					{
						"doctype": "Location",
						"location_name": land_unit.get("land_unit_name"),
						"parent_location": land_unit.get("parent_land_unit") or "All Land Units",
						"is_container": land_unit.get("is_container"),
						"is_group": land_unit.get("is_group"),
						"latitude": land_unit.get("latitude"),
						"longitude": land_unit.get("longitude"),
						"area": land_unit.get("area"),
						"location": land_unit.get("location"),
						"lft": land_unit.get("lft"),
						"rgt": land_unit.get("rgt"),
					}
				).insert(ignore_permissions=True)

	# Delete the Land Unit and Linked Land Unit doctypes
	if nts.db.table_exists("Land Unit"):
		nts.delete_doc("DocType", "Land Unit", force=1)

	if nts.db.table_exists("Linked Land Unit"):
		nts.delete_doc("DocType", "Linked Land Unit", force=1)
