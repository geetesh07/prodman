# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import nts 

test_records = nts .get_test_records("Cost Center")


class TestCostCenter(unittest.TestCase):
	def test_cost_center_creation_against_child_node(self):
		if not nts .db.get_value("Cost Center", {"name": "_Test Cost Center 2 - _TC"}):
			nts .get_doc(test_records[1]).insert()

		cost_center = nts .get_doc(
			{
				"doctype": "Cost Center",
				"cost_center_name": "_Test Cost Center 3",
				"parent_cost_center": "_Test Cost Center 2 - _TC",
				"is_group": 0,
				"company": "_Test Company",
			}
		)

		self.assertRaises(nts .ValidationError, cost_center.save)


def create_cost_center(**args):
	args = nts ._dict(args)
	if args.cost_center_name:
		company = args.company or "_Test Company"
		company_abbr = nts .db.get_value("Company", company, "abbr")
		cc_name = args.cost_center_name + " - " + company_abbr
		if not nts .db.exists("Cost Center", cc_name):
			cc = nts .new_doc("Cost Center")
			cc.company = args.company or "_Test Company"
			cc.cost_center_name = args.cost_center_name
			cc.is_group = args.is_group or 0
			cc.parent_cost_center = args.parent_cost_center or "_Test Company - _TC"
			cc.insert()
