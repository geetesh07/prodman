import click
import nts


def execute():
	if "education" in nts.get_installed_apps():
		return

	nts.delete_doc("Workspace", "Education", ignore_missing=True, force=True)

	pages = nts.get_all("Page", {"module": "education"}, pluck="name")
	for page in pages:
		nts.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = nts.get_all("Report", {"module": "education", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		nts.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = nts.get_all("Print Format", {"module": "education", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		nts.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	nts.reload_doc("website", "doctype", "website_settings")
	forms = nts.get_all("Web Form", {"module": "education", "is_standard": 1}, pluck="name")
	for form in forms:
		nts.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = nts.get_all("Dashboard", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		nts.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = nts.get_all("Dashboard Chart", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		nts.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	nts.reload_doc("desk", "doctype", "number_card")
	cards = nts.get_all("Number Card", {"module": "education", "is_standard": 1}, pluck="name")
	for card in cards:
		nts.delete_doc("Number Card", card, ignore_missing=True, force=True)

	doctypes = nts.get_all("DocType", {"module": "education", "custom": 0}, pluck="name")

	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	titles = [
		"Fees",
		"Student Admission",
		"Grant Application",
		"Chapter",
		"Certification Application",
	]
	items = nts.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		nts.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	nts.delete_doc("Module Def", "Education", ignore_missing=True, force=True)

	click.secho(
		"Education Module is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/nts/education",
		fg="yellow",
	)
