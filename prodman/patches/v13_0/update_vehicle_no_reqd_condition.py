import nts


def execute():
	nts.reload_doc("custom", "doctype", "custom_field", force=True)
	company = nts.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if nts.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		nts.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
