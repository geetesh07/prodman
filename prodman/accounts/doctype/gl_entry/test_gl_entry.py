# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import unittest

import nts 
from nts .model.naming import parse_naming_series

from prodman.accounts.doctype.gl_entry.gl_entry import rename_gle_sle_docs
from prodman.accounts.doctype.journal_entry.test_journal_entry import make_journal_entry


class TestGLEntry(unittest.TestCase):
	def test_round_off_entry(self):
		nts .db.set_value("Company", "_Test Company", "round_off_account", "_Test Write Off - _TC")
		nts .db.set_value("Company", "_Test Company", "round_off_cost_center", "_Test Cost Center - _TC")

		jv = make_journal_entry(
			"_Test Account Cost for Goods Sold - _TC",
			"_Test Bank - _TC",
			100,
			"_Test Cost Center - _TC",
			submit=False,
		)

		jv.get("accounts")[0].debit = 100.01
		jv.flags.ignore_validate = True
		jv.submit()

		round_off_entry = nts .db.sql(
			"""select name from `tabGL Entry`
			where voucher_type='Journal Entry' and voucher_no = %s
			and account='_Test Write Off - _TC' and cost_center='_Test Cost Center - _TC'
			and debit = 0 and credit = '.01'""",
			jv.name,
		)

		self.assertTrue(round_off_entry)

	def test_rename_entries(self):
		je = make_journal_entry(
			"_Test Account Cost for Goods Sold - _TC", "_Test Bank - _TC", 100, submit=True
		)
		rename_gle_sle_docs()
		naming_series = parse_naming_series(parts=nts .get_meta("GL Entry").autoname.split(".")[:-1])

		je = make_journal_entry(
			"_Test Account Cost for Goods Sold - _TC", "_Test Bank - _TC", 100, submit=True
		)

		gl_entries = nts .get_all(
			"GL Entry",
			fields=["name", "to_rename"],
			filters={"voucher_type": "Journal Entry", "voucher_no": je.name},
			order_by="creation",
		)

		self.assertTrue(all(entry.to_rename == 1 for entry in gl_entries))
		old_naming_series_current_value = nts .db.sql(
			"SELECT current from tabSeries where name = %s", naming_series
		)[0][0]

		rename_gle_sle_docs()

		new_gl_entries = nts .get_all(
			"GL Entry",
			fields=["name", "to_rename"],
			filters={"voucher_type": "Journal Entry", "voucher_no": je.name},
			order_by="creation",
		)
		self.assertTrue(all(entry.to_rename == 0 for entry in new_gl_entries))

		self.assertTrue(
			all(new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))
		)

		new_naming_series_current_value = nts .db.sql(
			"SELECT current from tabSeries where name = %s", naming_series
		)[0][0]
		self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)

	def test_validate_account_party_type(self):
		jv = make_journal_entry(
			"_Test Account Cost for Goods Sold - _TC",
			"_Test Bank - _TC",
			100,
			"_Test Cost Center - _TC",
			save=False,
			submit=False,
		)

		for row in jv.accounts:
			row.party_type = "Supplier"
			break

		jv.save()
		try:
			jv.submit()
		except Exception as e:
			self.assertEqual(
				str(e),
				"Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC",
			)

		jv1 = make_journal_entry(
			"_Test Account Cost for Goods Sold - _TC",
			"_Test Bank - _TC",
			100,
			"_Test Cost Center - _TC",
			save=False,
			submit=False,
		)

		for row in jv.accounts:
			row.party_type = "Customer"
			break

		jv1.save()
		try:
			jv1.submit()
		except Exception as e:
			self.assertEqual(
				str(e),
				"Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC",
			)

	def test_validate_account_party_type_shareholder(self):
		jv = make_journal_entry(
			"Opening Balance Equity - _TC",
			"Cash - _TC",
			100,
			"_Test Cost Center - _TC",
			save=False,
			submit=False,
		)

		for row in jv.accounts:
			row.party_type = "Shareholder"
			break

		jv.save().submit()
		self.assertEqual(1, jv.docstatus)
