import nts


def execute():
	nts.reload_doc("selling", "doctype", "sales_order_item", force=True)
	nts.reload_doc("buying", "doctype", "purchase_order_item", force=True)

	for doctype in ("Sales Order Item", "Purchase Order Item"):
		nts.db.sql(
			f"""
			UPDATE `tab{doctype}`
			SET against_blanket_order = 1
			WHERE ifnull(blanket_order, '') != ''
		"""
		)
