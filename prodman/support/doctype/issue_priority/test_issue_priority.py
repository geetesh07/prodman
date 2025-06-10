# Copyright (c) 2019, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts


class TestIssuePriority(unittest.TestCase):
	def test_priorities(self):
		make_priorities()
		priorities = nts.get_list("Issue Priority")

		for priority in priorities:
			self.assertIn(priority.name, ["Low", "Medium", "High"])


def make_priorities():
	insert_priority("Low")
	insert_priority("Medium")
	insert_priority("High")


def insert_priority(name):
	if not nts.db.exists("Issue Priority", name):
		nts.get_doc({"doctype": "Issue Priority", "name": name}).insert(ignore_permissions=True)
