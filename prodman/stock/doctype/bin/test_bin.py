# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase

from prodman.stock.doctype.item.test_item import make_item
from prodman.stock.utils import _create_bin


class TestBin(ntsTestCase):
	def test_concurrent_inserts(self):
		"""Ensure no duplicates are possible in case of concurrent inserts"""
		item_code = "_TestConcurrentBin"
		make_item(item_code)
		warehouse = "_Test Warehouse - _TC"

		bin1 = nts.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		bin1.insert()

		bin2 = nts.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		with self.assertRaises(nts.UniqueValidationError):
			bin2.insert()

		# util method should handle it
		bin = _create_bin(item_code, warehouse)
		self.assertEqual(bin.item_code, item_code)

		nts.db.rollback()

	def test_index_exists(self):
		indexes = nts.db.sql("show index from tabBin where Non_unique = 0", as_dict=1)
		if not any(index.get("Key_name") == "unique_item_warehouse" for index in indexes):
			self.fail("Expected unique index on item-warehouse")
