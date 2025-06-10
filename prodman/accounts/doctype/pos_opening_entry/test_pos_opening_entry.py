# Copyright (c) 2020, nts  Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts 


class TestPOSOpeningEntry(unittest.TestCase):
	pass


def create_opening_entry(pos_profile, user):
	entry = nts .new_doc("POS Opening Entry")
	entry.pos_profile = pos_profile.name
	entry.user = user
	entry.company = pos_profile.company
	entry.period_start_date = nts .utils.get_datetime()

	balance_details = []
	for d in pos_profile.payments:
		balance_details.append(nts ._dict({"mode_of_payment": d.mode_of_payment}))

	entry.set("balance_details", balance_details)
	entry.submit()

	return entry.as_dict()
