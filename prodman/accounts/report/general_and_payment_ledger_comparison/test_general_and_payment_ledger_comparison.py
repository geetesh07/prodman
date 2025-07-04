import nts 
from nts  import qb
from nts .tests.utils import nts TestCase
from nts .utils import add_days

from prodman.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from prodman.accounts.report.general_and_payment_ledger_comparison.general_and_payment_ledger_comparison import (
	execute,
)
from prodman.accounts.test.accounts_mixin import AccountsTestMixin


class TestGeneralAndPaymentLedger(nts TestCase, AccountsTestMixin):
	def setUp(self):
		self.create_company()
		self.cleanup()

	def tearDown(self):
		nts .db.rollback()

	def cleanup(self):
		doctypes = []
		doctypes.append(qb.DocType("GL Entry"))
		doctypes.append(qb.DocType("Payment Ledger Entry"))
		doctypes.append(qb.DocType("Sales Invoice"))

		for doctype in doctypes:
			qb.from_(doctype).delete().where(doctype.company == self.company).run()

	def test_01_basic_report_functionality(self):
		sinv = create_sales_invoice(
			company=self.company,
			debit_to=self.debit_to,
			expense_account=self.expense_account,
			cost_center=self.cost_center,
			income_account=self.income_account,
			warehouse=self.warehouse,
		)

		# manually edit the payment ledger entry
		ple = nts .db.get_all("Payment Ledger Entry", filters={"voucher_no": sinv.name, "delinked": 0})[0]
		nts .db.set_value("Payment Ledger Entry", ple.name, "amount", sinv.grand_total - 1)

		filters = nts ._dict({"company": self.company})
		columns, data = execute(filters=filters)
		self.assertEqual(len(data), 1)

		expected = {
			"company": sinv.company,
			"account": sinv.debit_to,
			"voucher_type": sinv.doctype,
			"voucher_no": sinv.name,
			"party_type": "Customer",
			"party": sinv.customer,
			"gl_balance": sinv.grand_total,
			"pl_balance": sinv.grand_total - 1,
		}
		self.assertEqual(expected, data[0])

		# account filter
		filters = nts ._dict({"company": self.company, "account": self.debit_to})
		columns, data = execute(filters=filters)
		self.assertEqual(len(data), 1)
		self.assertEqual(expected, data[0])

		filters = nts ._dict({"company": self.company, "account": self.creditors})
		columns, data = execute(filters=filters)
		self.assertEqual([], data)

		# voucher_no filter
		filters = nts ._dict({"company": self.company, "voucher_no": sinv.name})
		columns, data = execute(filters=filters)
		self.assertEqual(len(data), 1)
		self.assertEqual(expected, data[0])

		filters = nts ._dict({"company": self.company, "voucher_no": sinv.name + "-1"})
		columns, data = execute(filters=filters)
		self.assertEqual([], data)

		# date range filter
		filters = nts ._dict(
			{
				"company": self.company,
				"period_start_date": sinv.posting_date,
				"period_end_date": sinv.posting_date,
			}
		)
		columns, data = execute(filters=filters)
		self.assertEqual(len(data), 1)
		self.assertEqual(expected, data[0])

		filters = nts ._dict(
			{
				"company": self.company,
				"period_start_date": add_days(sinv.posting_date, -1),
				"period_end_date": add_days(sinv.posting_date, -1),
			}
		)
		columns, data = execute(filters=filters)
		self.assertEqual([], data)
