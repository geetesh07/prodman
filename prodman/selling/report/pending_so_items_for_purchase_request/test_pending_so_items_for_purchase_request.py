# Copyright (c) 2013, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.tests.utils import ntsTestCase
from nts.utils import add_months, nowdate

from prodman.selling.doctype.sales_order.sales_order import make_material_request
from prodman.selling.doctype.sales_order.test_sales_order import make_sales_order
from prodman.selling.report.pending_so_items_for_purchase_request.pending_so_items_for_purchase_request import (
	execute,
)


class TestPendingSOItemsForPurchaseRequest(ntsTestCase):
	def test_result_for_partial_material_request(self):
		so = make_sales_order()
		mr = make_material_request(so.name)
		mr.items[0].qty = 4
		mr.schedule_date = add_months(nowdate(), 1)
		mr.submit()
		report = execute()
		l = len(report[1])
		self.assertEqual((so.items[0].qty - mr.items[0].qty), report[1][l - 1]["pending_qty"])

	def test_result_for_so_item(self):
		so = make_sales_order()
		report = execute()
		l = len(report[1])
		self.assertEqual(so.items[0].qty, report[1][l - 1]["pending_qty"])
