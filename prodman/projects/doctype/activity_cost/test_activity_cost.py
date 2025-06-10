# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt

import unittest

import nts

from prodman.projects.doctype.activity_cost.activity_cost import DuplicationError


class TestActivityCost(unittest.TestCase):
	def test_duplication(self):
		nts.db.sql("delete from `tabActivity Cost`")
		activity_cost1 = nts.new_doc("Activity Cost")
		activity_cost1.update(
			{
				"employee": "_T-Employee-00001",
				"employee_name": "_Test Employee",
				"activity_type": "_Test Activity Type 1",
				"billing_rate": 100,
				"costing_rate": 50,
			}
		)
		activity_cost1.insert()
		activity_cost2 = nts.copy_doc(activity_cost1)
		self.assertRaises(DuplicationError, activity_cost2.insert)
		nts.db.sql("delete from `tabActivity Cost`")
