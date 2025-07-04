# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.test_runner import make_test_records

from prodman.accounts.party import get_due_date
from prodman.controllers.website_list_for_contact import get_customers_suppliers
from prodman.exceptions import PartyDisabled

test_dependencies = ["Payment Term", "Payment Terms Template"]
test_records = nts.get_test_records("Supplier")

from nts.tests.utils import ntsTestCase


class TestSupplier(ntsTestCase):
	def test_get_supplier_group_details(self):
		doc = nts.new_doc("Supplier Group")
		doc.supplier_group_name = "_Testing Supplier Group"
		doc.payment_terms = "_Test Payment Term Template 3"
		doc.accounts = []
		test_account_details = {
			"company": "_Test Company",
			"account": "Creditors - _TC",
		}
		doc.append("accounts", test_account_details)
		doc.save()
		s_doc = nts.new_doc("Supplier")
		s_doc.supplier_name = "Testing Supplier"
		s_doc.supplier_group = "_Testing Supplier Group"
		s_doc.payment_terms = ""
		s_doc.accounts = []
		s_doc.insert()
		s_doc.get_supplier_group_details()
		self.assertEqual(s_doc.payment_terms, "_Test Payment Term Template 3")
		self.assertEqual(s_doc.accounts[0].company, "_Test Company")
		self.assertEqual(s_doc.accounts[0].account, "Creditors - _TC")
		s_doc.delete()
		doc.delete()

	def test_supplier_default_payment_terms(self):
		# Payment Term based on Days after invoice date
		nts.db.set_value(
			"Supplier", "_Test Supplier With Template 1", "payment_terms", "_Test Payment Term Template 3"
		)

		due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2016-02-21")

		due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2017-02-21")

		# Payment Term based on last day of month
		nts.db.set_value(
			"Supplier", "_Test Supplier With Template 1", "payment_terms", "_Test Payment Term Template 1"
		)

		due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2016-02-29")

		due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2017-02-28")

		nts.db.set_value("Supplier", "_Test Supplier With Template 1", "payment_terms", "")

		# Set credit limit for the supplier group instead of supplier and evaluate the due date
		nts.db.set_value(
			"Supplier Group", "_Test Supplier Group", "payment_terms", "_Test Payment Term Template 3"
		)

		due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2016-02-21")

		# Payment terms for Supplier Group instead of supplier and evaluate the due date
		nts.db.set_value(
			"Supplier Group", "_Test Supplier Group", "payment_terms", "_Test Payment Term Template 1"
		)

		# Leap year
		due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2016-02-29")
		# # Non Leap year
		due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
		self.assertEqual(due_date, "2017-02-28")

		# Supplier with no default Payment Terms Template
		nts.db.set_value("Supplier Group", "_Test Supplier Group", "payment_terms", "")
		nts.db.set_value("Supplier", "_Test Supplier", "payment_terms", "")

		due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier")
		self.assertEqual(due_date, "2016-01-22")
		# # Non Leap year
		due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier")
		self.assertEqual(due_date, "2017-01-22")

	def test_supplier_disabled(self):
		make_test_records("Item")

		nts.db.set_value("Supplier", "_Test Supplier", "disabled", 1)

		from prodman.buying.doctype.purchase_order.test_purchase_order import create_purchase_order

		po = create_purchase_order(do_not_save=True)

		self.assertRaises(PartyDisabled, po.save)

		nts.db.set_value("Supplier", "_Test Supplier", "disabled", 0)

		po.save()

	def test_supplier_country(self):
		# Test that country field exists in Supplier DocType
		supplier = nts.get_doc("Supplier", "_Test Supplier with Country")
		self.assertTrue("country" in supplier.as_dict())

		# Test if test supplier field record is 'Greece'
		self.assertEqual(supplier.country, "Greece")

		# Test update Supplier instance country value
		supplier = nts.get_doc("Supplier", "_Test Supplier")
		supplier.country = "Greece"
		supplier.save()
		self.assertEqual(supplier.country, "Greece")

	def test_party_details_tax_category(self):
		from prodman.accounts.party import get_party_details

		nts.delete_doc_if_exists("Address", "_Test Address With Tax Category-Billing")

		# Tax Category without Address
		details = get_party_details("_Test Supplier With Tax Category", party_type="Supplier")
		self.assertEqual(details.tax_category, "_Test Tax Category 1")

		address = nts.get_doc(
			dict(
				doctype="Address",
				address_title="_Test Address With Tax Category",
				tax_category="_Test Tax Category 2",
				address_type="Billing",
				address_line1="Station Road",
				city="_Test City",
				country="India",
				links=[dict(link_doctype="Supplier", link_name="_Test Supplier With Tax Category")],
			)
		).insert()

		# Tax Category with Address
		details = get_party_details("_Test Supplier With Tax Category", party_type="Supplier")
		self.assertEqual(details.tax_category, "_Test Tax Category 2")

		# Rollback
		address.delete()


def create_supplier(**args):
	args = nts._dict(args)

	if not args.supplier_name:
		args.supplier_name = nts.generate_hash()

	if nts.db.exists("Supplier", args.supplier_name):
		return nts.get_doc("Supplier", args.supplier_name)

	doc = nts.get_doc(
		{
			"doctype": "Supplier",
			"supplier_name": args.supplier_name,
			"default_currency": args.default_currency,
			"supplier_type": args.supplier_type or "Company",
			"tax_withholding_category": args.tax_withholding_category,
		}
	)
	if not args.without_supplier_group:
		doc.supplier_group = args.supplier_group or "Services"

	doc.insert()

	return doc


class TestSupplierPortal(ntsTestCase):
	def test_portal_user_can_access_supplier_data(self):
		supplier = create_supplier()

		user = nts.generate_hash() + "@example.com"
		nts.new_doc(
			"User",
			first_name="Supplier Portal User",
			email=user,
			send_welcome_email=False,
		).insert()

		supplier.append("portal_users", {"user": user})
		supplier.save()

		nts.set_user(user)
		_, suppliers = get_customers_suppliers("Purchase Order", user)

		self.assertIn(supplier.name, suppliers)
