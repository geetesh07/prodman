import nts


def execute():
	"""Correct amount in child table of required items table."""

	nts.reload_doc("manufacturing", "doctype", "work_order")
	nts.reload_doc("manufacturing", "doctype", "work_order_item")

	nts.db.sql(
		"""UPDATE `tabWork Order Item` SET amount = ifnull(rate, 0.0) * ifnull(required_qty, 0.0)"""
	)
