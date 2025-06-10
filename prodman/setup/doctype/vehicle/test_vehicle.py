# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts
from nts.utils import random_string

# test_records = nts.get_test_records('Vehicle')


class TestVehicle(unittest.TestCase):
	def test_make_vehicle(self):
		vehicle = nts.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": nts.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": nts.utils.flt(500000),
			}
		)
		vehicle.insert()

	def test_renaming_vehicle(self):
		license_plate = random_string(10).upper()

		vehicle = nts.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": license_plate,
				"make": "Skoda",
				"model": "Slavia",
				"last_odometer": 5000,
				"acquisition_date": nts.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234EFGH",
				"uom": "Litre",
				"vehicle_value": nts.utils.flt(500000),
			}
		)
		vehicle.insert()

		new_license_plate = random_string(10).upper()
		nts.rename_doc("Vehicle", license_plate, new_license_plate)

		self.assertEqual(
			new_license_plate, nts.db.get_value("Vehicle", new_license_plate, "license_plate")
		)
