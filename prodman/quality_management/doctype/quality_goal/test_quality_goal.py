# Copyright (c) 2018, nts and Contributors
# See license.txt

import unittest

import nts


class TestQualityGoal(unittest.TestCase):
	def test_quality_goal(self):
		# no code, just a basic sanity check
		goal = get_quality_goal()
		self.assertTrue(goal)
		goal.delete()


def get_quality_goal():
	return nts.get_doc(
		dict(
			doctype="Quality Goal",
			goal="Test Quality Module",
			frequency="Daily",
			objectives=[dict(objective="Check test cases", target="100", uom="Percent")],
		)
	).insert()
