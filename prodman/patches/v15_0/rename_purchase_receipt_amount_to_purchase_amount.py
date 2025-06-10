import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("assets", "doctype", "asset")
	if nts.db.has_column("Asset", "purchase_receipt_amount"):
		rename_field("Asset", "purchase_receipt_amount", "purchase_amount")
