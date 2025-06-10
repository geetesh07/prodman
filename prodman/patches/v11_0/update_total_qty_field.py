import nts


def execute():
	nts.reload_doc("buying", "doctype", "purchase_order")
	nts.reload_doc("buying", "doctype", "supplier_quotation")
	nts.reload_doc("selling", "doctype", "sales_order")
	nts.reload_doc("selling", "doctype", "quotation")
	nts.reload_doc("stock", "doctype", "delivery_note")
	nts.reload_doc("stock", "doctype", "purchase_receipt")
	nts.reload_doc("accounts", "doctype", "sales_invoice")
	nts.reload_doc("accounts", "doctype", "purchase_invoice")

	doctypes = [
		"Sales Order",
		"Sales Invoice",
		"Delivery Note",
		"Purchase Order",
		"Purchase Invoice",
		"Purchase Receipt",
		"Quotation",
		"Supplier Quotation",
	]

	for doctype in doctypes:
		total_qty = nts.db.sql(
			f"""
			SELECT
				parent, SUM(qty) as qty
			FROM
				`tab{doctype} Item`
			where parenttype = '{doctype}'
			GROUP BY parent
		""",
			as_dict=True,
		)

		# Query to update total_qty might become too big, Update in batches
		# batch_size is chosen arbitrarily, Don't try too hard to reason about it
		batch_size = 100000
		for i in range(0, len(total_qty), batch_size):
			batch_transactions = total_qty[i : i + batch_size]

			# UPDATE with CASE for some reason cannot use PRIMARY INDEX,
			# causing all rows to be examined, leading to a very slow update

			# UPDATE with WHERE clause uses PRIMARY INDEX, but will lead to too many queries

			# INSERT with ON DUPLICATE KEY UPDATE uses PRIMARY INDEX
			# and can perform multiple updates per query
			# This is probably never used anywhere else as of now, but should be
			values = []
			for d in batch_transactions:
				values.append(f"({nts.db.escape(d.parent)}, {d.qty})")
			conditions = ",".join(values)
			nts.db.sql(
				f"""
				INSERT INTO `tab{doctype}` (name, total_qty) VALUES {conditions}
				ON DUPLICATE KEY UPDATE name = VALUES(name), total_qty = VALUES(total_qty)
			"""
			)
