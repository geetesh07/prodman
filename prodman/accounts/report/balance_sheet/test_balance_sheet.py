# Copyright (c) 2023, nts  Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import nts 
from nts .tests.utils import nts TestCase
from nts .utils import today

from prodman.accounts.report.balance_sheet.balance_sheet import execute


class TestBalanceSheet(nts TestCase):
	def test_balance_sheet(self):
		from prodman.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice
		from prodman.accounts.doctype.sales_invoice.test_sales_invoice import (
			create_sales_invoice,
		)

		nts .db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
		nts .db.sql("delete from `tabSales Invoice` where company='_Test Company 6'")
		nts .db.sql("delete from `tabGL Entry` where company='_Test Company 6'")

		make_purchase_invoice(
			company="_Test Company 6",
			warehouse="Finished Goods - _TC6",
			expense_account="Cost of Goods Sold - _TC6",
			cost_center="Main - _TC6",
			qty=10,
			rate=100,
		)
		create_sales_invoice(
			company="_Test Company 6",
			debit_to="Debtors - _TC6",
			income_account="Sales - _TC6",
			cost_center="Main - _TC6",
			qty=5,
			rate=110,
		)
		filters = nts ._dict(
			company="_Test Company 6",
			period_start_date=today(),
			period_end_date=today(),
			periodicity="Yearly",
		)
		result = execute(filters)[1]
		for account_dict in result:
			if account_dict.get("account") == "Current Liabilities - _TC6":
				self.assertEqual(account_dict.total, 1000)
			if account_dict.get("account") == "Current Assets - _TC6":
				self.assertEqual(account_dict.total, 550)
