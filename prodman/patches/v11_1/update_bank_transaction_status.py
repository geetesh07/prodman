# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("accounts", "doctype", "bank_transaction")

	bank_transaction_fields = nts.get_meta("Bank Transaction").get_valid_columns()

	if "debit" in bank_transaction_fields:
		nts.db.sql(
			""" UPDATE `tabBank Transaction`
            SET status = 'Reconciled'
            WHERE
                status = 'Settled' and (debit = allocated_amount or credit = allocated_amount)
                and ifnull(allocated_amount, 0) > 0
        """
		)

	elif "deposit" in bank_transaction_fields:
		nts.db.sql(
			""" UPDATE `tabBank Transaction`
            SET status = 'Reconciled'
            WHERE
                status = 'Settled' and (deposit = allocated_amount or withdrawal = allocated_amount)
                and ifnull(allocated_amount, 0) > 0
        """
		)
