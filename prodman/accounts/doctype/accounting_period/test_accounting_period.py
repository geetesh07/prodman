# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts 
from nts .utils import add_months, nowdate

from prodman.accounts.doctype.accounting_period.accounting_period import (
	ClosedAccountingPeriod,
	OverlapError,
)
from prodman.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice

test_dependencies = ["Item"]


class TestAccountingPeriod(unittest.TestCase):
	def test_overlap(self):
		ap1 = create_accounting_period(
			start_date="2018-04-01", end_date="2018-06-30", company="Wind Power LLC"
		)
		ap1.save()

		ap2 = create_accounting_period(
			start_date="2018-06-30",
			end_date="2018-07-10",
			company="Wind Power LLC",
			period_name="Test Accounting Period 1",
		)
		self.assertRaises(OverlapError, ap2.save)

	def test_accounting_period(self):
		ap1 = create_accounting_period(period_name="Test Accounting Period 2")
		ap1.save()

		doc = create_sales_invoice(do_not_save=1, cost_center="_Test Company - _TC", warehouse="Stores - _TC")
		self.assertRaises(ClosedAccountingPeriod, doc.save)

	def tearDown(self):
		for d in nts .get_all("Accounting Period"):
			nts .delete_doc("Accounting Period", d.name)


def create_accounting_period(**args):
	args = nts ._dict(args)

	accounting_period = nts .new_doc("Accounting Period")
	accounting_period.start_date = args.start_date or nowdate()
	accounting_period.end_date = args.end_date or add_months(nowdate(), 1)
	accounting_period.company = args.company or "_Test Company"
	accounting_period.period_name = args.period_name or "_Test_Period_Name_1"
	accounting_period.append("closed_documents", {"document_type": "Sales Invoice", "closed": 1})

	return accounting_period
