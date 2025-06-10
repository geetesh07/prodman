# Copyright (c) 2021, nts and Contributors
# License: GNU General Public License v3. See license.txt
import nts

from prodman.controllers.status_updater import OverAllowanceError


def execute():
	nts.reload_doc("stock", "doctype", "purchase_receipt")
	nts.reload_doc("stock", "doctype", "purchase_receipt_item")
	nts.reload_doc("stock", "doctype", "delivery_note")
	nts.reload_doc("stock", "doctype", "delivery_note_item")
	nts.reload_doc("stock", "doctype", "stock_settings")

	def update_from_return_docs(doctype):
		for return_doc in nts.get_all(
			doctype, filters={"is_return": 1, "docstatus": 1, "return_against": ("!=", "")}
		):
			# Update original receipt/delivery document from return
			return_doc = nts.get_cached_doc(doctype, return_doc.name)
			try:
				return_doc.update_prevdoc_status()
			except OverAllowanceError:
				nts.db.rollback()
				continue

			return_against = nts.get_doc(doctype, return_doc.return_against)
			return_against.update_billing_status()
			nts.db.commit()

	# Set received qty in stock uom in PR, as returned qty is checked against it
	nts.db.sql(
		""" update `tabPurchase Receipt Item`
		set received_stock_qty = received_qty * conversion_factor
		where docstatus = 1 """
	)

	for doctype in ("Purchase Receipt", "Delivery Note"):
		update_from_return_docs(doctype)
