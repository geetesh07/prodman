import nts


def execute():
	nts.reload_doc("stock", "doctype", "shipment")

	# update submitted status
	nts.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Submitted"
					WHERE status = "Draft" AND docstatus = 1"""
	)

	# update cancelled status
	nts.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Cancelled"
					WHERE status = "Draft" AND docstatus = 2"""
	)
