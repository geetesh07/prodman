# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt


import nts

test_records = nts.get_test_records("Item Attribute")

from nts.tests.utils import ntsTestCase

from prodman.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError


class TestItemAttribute(ntsTestCase):
	def setUp(self):
		super().setUp()
		if nts.db.exists("Item Attribute", "_Test_Length"):
			nts.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = nts.get_doc(
			{
				"doctype": "Item Attribute",
				"attribute_name": "_Test_Length",
				"numeric_values": 1,
				"from_range": 0.0,
				"to_range": 100.0,
				"increment": 0,
			}
		)

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()
