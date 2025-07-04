import nts
from nts import _
from nts.utils.nestedset import rebuild_tree


def execute():
	nts.local.lang = nts.db.get_default("lang") or "en"

	for doctype in ["department", "leave_period", "staffing_plan", "job_opening"]:
		nts.reload_doc("hr", "doctype", doctype)
	nts.reload_doc("Payroll", "doctype", "payroll_entry")

	companies = nts.db.get_all("Company", fields=["name", "abbr"])
	departments = nts.db.get_all("Department")
	comp_dict = {}

	# create a blank list for each company
	for company in companies:
		comp_dict[company.name] = {}

	for department in departments:
		# skip root node
		if _(department.name) == _("All Departments"):
			continue

		# for each company, create a copy of the doc
		department_doc = nts.get_doc("Department", department)
		for company in companies:
			copy_doc = nts.copy_doc(department_doc)
			copy_doc.update({"company": company.name})
			try:
				copy_doc.insert()
			except nts.DuplicateEntryError:
				pass
			# append list of new department for each company
			comp_dict[company.name][department.name] = copy_doc.name

	rebuild_tree("Department", "parent_department")
	doctypes = ["Asset", "Employee", "Payroll Entry", "Staffing Plan", "Job Opening"]

	for d in doctypes:
		update_records(d, comp_dict)

	update_instructors(comp_dict)

	nts.local.lang = "en"


def update_records(doctype, comp_dict):
	when_then = []
	for company in comp_dict:
		records = comp_dict[company]

		for department in records:
			when_then.append(
				f"""
				WHEN company = "{company}" and department = "{department}"
				THEN "{records[department]}"
			"""
			)

	if not when_then:
		return

	nts.db.sql(
		"""
		update
			`tab{}`
		set
			department = CASE {} END
	""".format(doctype, " ".join(when_then))
	)


def update_instructors(comp_dict):
	when_then = []
	emp_details = nts.get_all("Employee", fields=["name", "company"])

	for employee in emp_details:
		records = comp_dict[employee.company] if employee.company else []

		for department in records:
			when_then.append(
				f"""
				WHEN employee = "{employee.name}" and department = "{department}"
				THEN "{records[department]}"
			"""
			)

	if not when_then:
		return

	nts.db.sql(
		"""
		update
			`tabInstructor`
		set
			department = CASE %s END
	"""
		% (" ".join(when_then))
	)
