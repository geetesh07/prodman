# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import nts

test_ignore = ["Leave Block List"]


class TestDepartment(unittest.TestCase):
	def test_remove_department_data(self):
		doc = create_department("Test Department")
		nts.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None):
	doc = nts.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": nts.defaults.get_defaults().company,
		}
	).insert()

	return doc


test_records = nts.get_test_records("Department")
