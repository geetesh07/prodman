import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("stock", "doctype", "item")
	nts.reload_doc("stock", "doctype", "stock_settings")
	nts.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = nts.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	nts.db.set_single_value("Accounts Settings", "over_delivery_receipt_allowance", qty_allowance)

	nts.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
