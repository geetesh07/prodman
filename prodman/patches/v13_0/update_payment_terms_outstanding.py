# Copyright (c) 2020, nts Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import nts


def execute():
	nts.reload_doc("accounts", "doctype", "Payment Schedule")
	if nts.db.count("Payment Schedule"):
		nts.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
