import nts


def execute():
	if "healthcare" in nts.get_installed_apps():
		return

	nts.delete_doc("Workspace", "Healthcare", ignore_missing=True, force=True)

	pages = nts.get_all("Page", {"module": "healthcare"}, pluck="name")
	for page in pages:
		nts.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = nts.get_all("Report", {"module": "healthcare", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		nts.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = nts.get_all("Print Format", {"module": "healthcare", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		nts.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	nts.reload_doc("website", "doctype", "website_settings")
	forms = nts.get_all("Web Form", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for form in forms:
		nts.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = nts.get_all("Dashboard", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		nts.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = nts.get_all("Dashboard Chart", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		nts.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	nts.reload_doc("desk", "doctype", "number_card")
	cards = nts.get_all("Number Card", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for card in cards:
		nts.delete_doc("Number Card", card, ignore_missing=True, force=True)

	titles = ["Lab Test", "Prescription", "Patient Appointment", "Patient"]
	items = nts.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		nts.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	doctypes = nts.get_all("DocType", {"module": "healthcare", "custom": 0}, pluck="name")
	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	nts.delete_doc("Module Def", "Healthcare", ignore_missing=True, force=True)

	custom_fields = {
		"Sales Invoice": ["patient", "patient_name", "ref_practitioner"],
		"Sales Invoice Item": ["reference_dt", "reference_dn"],
		"Stock Entry": ["inpatient_medication_entry"],
		"Stock Entry Detail": ["patient", "inpatient_medication_entry_child"],
	}
	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = nts.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			nts.delete_doc("Custom Field", record, ignore_missing=True, force=True)
