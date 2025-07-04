# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.tests.utils import ntsTestCase, change_settings
from nts.utils import add_days, today

from prodman.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order
from prodman.controllers.accounts_controller import InvalidQtyError


class TestPurchaseOrder(ntsTestCase):
	def test_supplier_quotation_qty(self):
		sq = nts.copy_doc(test_records[0])
		sq.items[0].qty = 0
		with self.assertRaises(InvalidQtyError):
			sq.save()

		# No error with qty=1
		sq.items[0].qty = 1
		sq.save()
		self.assertEqual(sq.items[0].qty, 1)

	def test_make_purchase_order(self):
		sq = nts.copy_doc(test_records[0]).insert()

		self.assertRaises(nts.ValidationError, make_purchase_order, sq.name)

		sq = nts.get_doc("Supplier Quotation", sq.name)
		sq.submit()
		po = make_purchase_order(sq.name)

		self.assertEqual(po.doctype, "Purchase Order")
		self.assertEqual(len(po.get("items")), len(sq.get("items")))

		po.naming_series = "_T-Purchase Order-"

		for doc in po.get("items"):
			if doc.get("item_code"):
				doc.set("schedule_date", add_days(today(), 1))

		po.insert()

	@change_settings("Buying Settings", {"allow_zero_qty_in_supplier_quotation": 1})
	def test_map_purchase_order_from_zero_qty_supplier_quotation(self):
		sq = nts.copy_doc(test_records[0]).insert()
		sq.items[0].qty = 0
		sq.submit()

		po = make_purchase_order(sq.name)
		self.assertEqual(len(po.get("items")), 1)
		self.assertEqual(po.get("items")[0].qty, 0)
		self.assertEqual(po.get("items")[0].item_code, sq.get("items")[0].item_code)


test_records = nts.get_test_records("Supplier Quotation")
