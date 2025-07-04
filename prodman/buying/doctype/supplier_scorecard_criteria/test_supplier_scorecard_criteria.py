# Copyright (c) 2017, nts Technologies Pvt. Ltd. and Contributors
# See license.txt


import nts
from nts.tests.utils import ntsTestCase


class TestSupplierScorecardCriteria(ntsTestCase):
	def test_variables_exist(self):
		delete_test_scorecards()
		for d in test_good_criteria:
			nts.get_doc(d).insert()

		self.assertRaises(nts.ValidationError, nts.get_doc(test_bad_criteria[0]).insert)

	def test_formula_validate(self):
		delete_test_scorecards()
		self.assertRaises(nts.ValidationError, nts.get_doc(test_bad_criteria[1]).insert)
		self.assertRaises(nts.ValidationError, nts.get_doc(test_bad_criteria[2]).insert)


def delete_test_scorecards():
	# Delete all the periods so we can delete all the criteria
	nts.db.sql("""delete from `tabSupplier Scorecard Period`""")
	nts.db.sql(
		"""delete from `tabSupplier Scorecard Scoring Criteria` where parenttype = 'Supplier Scorecard Period'"""
	)
	nts.db.sql(
		"""delete from `tabSupplier Scorecard Scoring Standing` where parenttype = 'Supplier Scorecard Period'"""
	)
	nts.db.sql(
		"""delete from `tabSupplier Scorecard Scoring Variable` where parenttype = 'Supplier Scorecard Period'"""
	)

	for d in test_good_criteria:
		if nts.db.exists("Supplier Scorecard Criteria", d.get("name")):
			# Delete all the periods, then delete the scorecard
			nts.delete_doc(d.get("doctype"), d.get("name"))

	for d in test_bad_criteria:
		if nts.db.exists("Supplier Scorecard Criteria", d.get("name")):
			# Delete all the periods, then delete the scorecard
			nts.delete_doc(d.get("doctype"), d.get("name"))


test_good_criteria = [
	{
		"name": "Delivery",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",
		"criteria_name": "Delivery",
		"max_score": 100.0,
	},
]

test_bad_criteria = [
	{
		"name": "Fake Criteria 1",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({fake_variable} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",  # Invalid variable name
		"criteria_name": "Fake Criteria 1",
		"max_score": 100.0,
	},
	{
		"name": "Fake Criteria 2",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} / {tot_cost_shipments}))* 100",  # Force 0 divided by 0
		"criteria_name": "Fake Criteria 2",
		"max_score": 100.0,
	},
	{
		"name": "Fake Criteria 3",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} {cost_of_on_time_shipments} / {tot_cost_shipments}))* 100",  # Two variables beside eachother
		"criteria_name": "Fake Criteria 3",
		"max_score": 100.0,
	},
]
