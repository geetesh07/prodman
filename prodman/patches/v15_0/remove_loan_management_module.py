import nts


def execute():
	if "lending" in nts.get_installed_apps():
		return

	nts.delete_doc("Module Def", "Loan Management", ignore_missing=True, force=True)

	nts.delete_doc("Workspace", "Loans", ignore_missing=True, force=True)

	print_formats = nts.get_all(
		"Print Format", {"module": "Loan Management", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		nts.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = nts.get_all("Report", {"module": "Loan Management", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		nts.delete_doc("Report", report, ignore_missing=True, force=True)

	doctypes = nts.get_all("DocType", {"module": "Loan Management", "custom": 0}, pluck="name")
	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True, force=True)

	notifications = nts.get_all(
		"Notification", {"module": "Loan Management", "is_standard": 1}, pluck="name"
	)
	for notifcation in notifications:
		nts.delete_doc("Notification", notifcation, ignore_missing=True, force=True)

	for dt in ["Web Form", "Dashboard", "Dashboard Chart", "Number Card"]:
		records = nts.get_all(dt, {"module": "Loan Management", "is_standard": 1}, pluck="name")
		for record in records:
			nts.delete_doc(dt, record, ignore_missing=True, force=True)

	custom_fields = {
		"Loan": ["repay_from_salary"],
		"Loan Repayment": ["repay_from_salary", "payroll_payable_account"],
	}

	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = nts.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			nts.delete_doc("Custom Field", record, ignore_missing=True, force=True)
