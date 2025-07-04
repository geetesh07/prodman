# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts 

from prodman.selling.doctype.sales_order.test_sales_order import make_sales_order

test_dependencies = ["Item"]


def test_create_test_data():
	nts .set_user("Administrator")
	# create test item
	if not nts .db.exists("Item", "_Test Tesla Car"):
		item = nts .get_doc(
			{
				"description": "_Test Tesla Car",
				"doctype": "Item",
				"has_batch_no": 0,
				"has_serial_no": 0,
				"inspection_required": 0,
				"is_stock_item": 1,
				"opening_stock": 100,
				"is_sub_contracted_item": 0,
				"item_code": "_Test Tesla Car",
				"item_group": "_Test Item Group",
				"item_name": "_Test Tesla Car",
				"apply_warehouse_wise_reorder_level": 0,
				"warehouse": "Stores - _TC",
				"valuation_rate": 5000,
				"standard_rate": 5000,
				"item_defaults": [
					{
						"company": "_Test Company",
						"default_warehouse": "Stores - _TC",
						"default_price_list": "_Test Price List",
						"expense_account": "Cost of Goods Sold - _TC",
						"buying_cost_center": "Main - _TC",
						"selling_cost_center": "Main - _TC",
						"income_account": "Sales - _TC",
					}
				],
			}
		)
		item.insert()
	# create test item price
	item_price = nts .get_list(
		"Item Price",
		filters={"item_code": "_Test Tesla Car", "price_list": "_Test Price List"},
		fields=["name"],
	)
	if len(item_price) == 0:
		item_price = nts .get_doc(
			{
				"doctype": "Item Price",
				"item_code": "_Test Tesla Car",
				"price_list": "_Test Price List",
				"price_list_rate": 5000,
			}
		)
		item_price.insert()
	# create test item pricing rule
	if not nts .db.exists("Pricing Rule", {"title": "_Test Pricing Rule for _Test Item"}):
		item_pricing_rule = nts .get_doc(
			{
				"doctype": "Pricing Rule",
				"title": "_Test Pricing Rule for _Test Item",
				"apply_on": "Item Code",
				"items": [{"item_code": "_Test Tesla Car"}],
				"warehouse": "Stores - _TC",
				"coupon_code_based": 1,
				"selling": 1,
				"rate_or_discount": "Discount Percentage",
				"discount_percentage": 30,
				"company": "_Test Company",
				"currency": "INR",
				"for_price_list": "_Test Price List",
			}
		)
		item_pricing_rule.insert()
	# create test item sales partner
	if not nts .db.exists("Sales Partner", "_Test Coupon Partner"):
		sales_partner = nts .get_doc(
			{
				"doctype": "Sales Partner",
				"partner_name": "_Test Coupon Partner",
				"commission_rate": 2,
				"referral_code": "COPART",
			}
		)
		sales_partner.insert()
	# create test item coupon code
	if not nts .db.exists("Coupon Code", "SAVE30"):
		pricing_rule = nts .db.get_value(
			"Pricing Rule", {"title": "_Test Pricing Rule for _Test Item"}, ["name"]
		)
		coupon_code = nts .get_doc(
			{
				"doctype": "Coupon Code",
				"coupon_name": "SAVE30",
				"coupon_code": "SAVE30",
				"pricing_rule": pricing_rule,
				"valid_from": "2014-01-01",
				"maximum_use": 1,
				"used": 0,
			}
		)
		coupon_code.insert()


class TestCouponCode(unittest.TestCase):
	def setUp(self):
		test_create_test_data()

	def tearDown(self):
		nts .set_user("Administrator")

	def test_sales_order_with_coupon_code(self):
		nts .db.set_value("Coupon Code", "SAVE30", "used", 0)

		so = make_sales_order(
			company="_Test Company",
			warehouse="Stores - _TC",
			customer="_Test Customer",
			selling_price_list="_Test Price List",
			item_code="_Test Tesla Car",
			rate=5000,
			qty=1,
			do_not_save=True,
		)

		self.assertEqual(so.items[0].rate, 5000)

		so.coupon_code = "SAVE30"
		so.sales_partner = "_Test Coupon Partner"
		so.save()

		# check item price after coupon code is applied
		self.assertEqual(so.items[0].rate, 3500)

		so.submit()
		self.assertEqual(nts .db.get_value("Coupon Code", "SAVE30", "used"), 1)
