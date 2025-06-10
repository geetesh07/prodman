# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts
from nts.utils import now

from prodman.assets.doctype.asset.test_asset import create_asset_data
from prodman.setup.doctype.employee.test_employee import make_employee
from prodman.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt


class TestAssetMovement(unittest.TestCase):
	def setUp(self):
		nts.db.set_value(
			"Company", "_Test Company", "capital_work_in_progress_account", "CWIP Account - _TC"
		)
		create_asset_data()
		make_location()

	def test_movement(self):
		pr = make_purchase_receipt(item_code="Macbook Pro", qty=1, rate=100000.0, location="Test Location")

		asset_name = nts.db.get_value("Asset", {"purchase_receipt": pr.name}, "name")
		asset = nts.get_doc("Asset", asset_name)
		asset.calculate_depreciation = 1
		asset.available_for_use_date = "2020-06-06"
		asset.purchase_date = "2020-06-06"
		asset.append(
			"finance_books",
			{
				"expected_value_after_useful_life": 10000,
				"next_depreciation_date": "2020-12-31",
				"depreciation_method": "Straight Line",
				"total_number_of_depreciations": 3,
				"frequency_of_depreciation": 10,
			},
		)

		if asset.docstatus == 0:
			asset.submit()

		# check asset movement is created
		if not nts.db.exists("Location", "Test Location 2"):
			nts.get_doc({"doctype": "Location", "location_name": "Test Location 2"}).insert()

		create_asset_movement(
			purpose="Transfer",
			company=asset.company,
			assets=[
				{
					"asset": asset.name,
					"source_location": "Test Location",
					"target_location": "Test Location 2",
				}
			],
			reference_doctype="Purchase Receipt",
			reference_name=pr.name,
		)
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location 2")

		movement1 = create_asset_movement(
			purpose="Transfer",
			company=asset.company,
			assets=[
				{
					"asset": asset.name,
					"source_location": "Test Location 2",
					"target_location": "Test Location",
				}
			],
			reference_doctype="Purchase Receipt",
			reference_name=pr.name,
		)
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location")

		movement1.cancel()
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location 2")

		employee = make_employee("testassetmovemp@example.com", company="_Test Company")
		create_asset_movement(
			purpose="Issue",
			company=asset.company,
			assets=[{"asset": asset.name, "source_location": "Test Location 2", "to_employee": employee}],
			reference_doctype="Purchase Receipt",
			reference_name=pr.name,
		)

		# after issuing, asset should belong to an employee not at a location
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), None)
		self.assertEqual(nts.db.get_value("Asset", asset.name, "custodian"), employee)

		create_asset_movement(
			purpose="Receipt",
			company=asset.company,
			assets=[{"asset": asset.name, "from_employee": employee, "target_location": "Test Location"}],
			reference_doctype="Purchase Receipt",
			reference_name=pr.name,
		)

		# after receiving, asset should belong to a location not at an employee
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location")

	def test_last_movement_cancellation(self):
		pr = make_purchase_receipt(item_code="Macbook Pro", qty=1, rate=100000.0, location="Test Location")

		asset_name = nts.db.get_value("Asset", {"purchase_receipt": pr.name}, "name")
		asset = nts.get_doc("Asset", asset_name)
		asset.calculate_depreciation = 1
		asset.available_for_use_date = "2020-06-06"
		asset.purchase_date = "2020-06-06"
		asset.append(
			"finance_books",
			{
				"expected_value_after_useful_life": 10000,
				"next_depreciation_date": "2020-12-31",
				"depreciation_method": "Straight Line",
				"total_number_of_depreciations": 3,
				"frequency_of_depreciation": 10,
			},
		)
		if asset.docstatus == 0:
			asset.submit()

		if not nts.db.exists("Location", "Test Location 2"):
			nts.get_doc({"doctype": "Location", "location_name": "Test Location 2"}).insert()

		movement = nts.get_doc({"doctype": "Asset Movement", "reference_name": pr.name})
		self.assertRaises(nts.ValidationError, movement.cancel)

		movement1 = create_asset_movement(
			purpose="Transfer",
			company=asset.company,
			assets=[
				{
					"asset": asset.name,
					"source_location": "Test Location",
					"target_location": "Test Location 2",
				}
			],
			reference_doctype="Purchase Receipt",
			reference_name=pr.name,
		)
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location 2")

		movement1.cancel()
		self.assertEqual(nts.db.get_value("Asset", asset.name, "location"), "Test Location")


def create_asset_movement(**args):
	args = nts._dict(args)

	if not args.transaction_date:
		args.transaction_date = now()

	movement = nts.new_doc("Asset Movement")
	movement.update(
		{
			"assets": args.assets,
			"transaction_date": args.transaction_date,
			"company": args.company,
			"purpose": args.purpose or "Receipt",
			"reference_doctype": args.reference_doctype,
			"reference_name": args.reference_name,
		}
	)

	movement.insert()
	movement.submit()

	return movement


def make_location():
	for location in ["Pune", "Mumbai", "Nagpur"]:
		if not nts.db.exists("Location", location):
			nts.get_doc({"doctype": "Location", "location_name": location}).insert(ignore_permissions=True)
