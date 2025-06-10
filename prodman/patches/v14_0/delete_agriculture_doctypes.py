import nts


def execute():
	if "agriculture" in nts.get_installed_apps():
		return

	nts.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	nts.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = nts.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		nts.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = nts.get_all("Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		nts.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = nts.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	nts.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
