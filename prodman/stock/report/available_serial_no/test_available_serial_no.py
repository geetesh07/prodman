# Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase
from nts.utils import add_days, today

from prodman.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from prodman.stock.doctype.item.test_item import create_item
from prodman.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt


class TestStockLedgerReport(ntsTestCase):
	def setUp(self) -> None:
		item = create_item("_Test Item with Serial No", is_stock_item=1)
		item.has_serial_no = 1
		item.serial_no_series = "TEST.###"
		item.save(ignore_permissions=True)

		self.filters = nts._dict(
			company="_Test Company",
			from_date=today(),
			to_date=add_days(today(), 30),
			item_code="_Test Item With Serial No",
		)

	def tearDown(self) -> None:
		nts.db.rollback()

	def test_available_serial_no(self):
		report = nts.get_doc("Report", "Available Serial No")

		make_purchase_receipt(qty=10, item_code="_Test Item with Serial No")
		data = report.get_data(filters=self.filters)
		serial_nos = [item for item in data[-1][-1]["balance_serial_no"].split("\n")]

		# Test 1: Since we have created an inward entry with Purchase Receipt of 10 qty, we should have 10 serial nos
		self.assertEqual(len(serial_nos), 10)

		create_delivery_note(qty=5, item_code="_Test Item with Serial No")
		data = report.get_data(filters=self.filters)
		serial_nos = [item for item in data[-1][-1]["balance_serial_no"].split("\n")]

		# Test 2: Since we have created a delivery note of 5 qty, we should have 5 serial nos
		self.assertEqual(len(serial_nos), 5)
