# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import nts
import nts.utils

import prodman
from prodman.setup.doctype.employee.employee import InactiveEmployeeStatusError

test_records = nts.get_test_records("Employee")


class TestEmployee(unittest.TestCase):
	def test_employee_status_left(self):
		employee1 = make_employee("test_employee_1@company.com")
		employee2 = make_employee("test_employee_2@company.com")
		employee1_doc = nts.get_doc("Employee", employee1)
		employee2_doc = nts.get_doc("Employee", employee2)
		employee2_doc.reload()
		employee2_doc.reports_to = employee1_doc.name
		employee2_doc.save()
		employee1_doc.reload()
		employee1_doc.status = "Left"
		self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)

	def test_user_has_employee(self):
		employee = make_employee("test_emp_user_creation@company.com")
		employee_doc = nts.get_doc("Employee", employee)
		user = employee_doc.user_id
		self.assertTrue("Employee" in nts.get_roles(user))
		employee_doc.user_id = ""
		employee_doc.save()
		self.assertTrue("Employee" not in nts.get_roles(user))

	def tearDown(self):
		nts.db.rollback()


def make_employee(user, company=None, **kwargs):
	if not nts.db.get_value("User", user):
		nts.get_doc(
			{
				"doctype": "User",
				"email": user,
				"first_name": user,
				"new_password": "password",
				"send_welcome_email": 0,
				"roles": [{"doctype": "Has Role", "role": "Employee"}],
			}
		).insert()

	if not nts.db.get_value("Employee", {"user_id": user}):
		employee = nts.get_doc(
			{
				"doctype": "Employee",
				"naming_series": "EMP-",
				"first_name": user,
				"company": company or prodman.get_default_company(),
				"user_id": user,
				"date_of_birth": "1990-05-08",
				"date_of_joining": "2013-01-01",
				"department": nts.get_all("Department", fields="name")[0].name,
				"gender": "Female",
				"company_email": user,
				"prefered_contact_email": "Company Email",
				"prefered_email": user,
				"status": "Active",
				"employment_type": "Intern",
			}
		)
		if kwargs:
			employee.update(kwargs)
		employee.insert()
		return employee.name
	else:
		employee = nts.get_doc("Employee", {"employee_name": user})
		employee.update(kwargs)
		employee.status = "Active"
		employee.save()
		return employee.name
