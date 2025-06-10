# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts 


class TestModeofPayment(unittest.TestCase):
	pass


def set_default_account_for_mode_of_payment(mode_of_payment, company, account):
	mode_of_payment.reload()
	if nts .db.exists(
		"Mode of Payment Account", {"parent": mode_of_payment.mode_of_payment, "company": company}
	):
		nts .db.set_value(
			"Mode of Payment Account",
			{"parent": mode_of_payment.mode_of_payment, "company": company},
			"default_account",
			account,
		)
		return

	mode_of_payment.append("accounts", {"company": company, "default_account": account})
	mode_of_payment.save()
