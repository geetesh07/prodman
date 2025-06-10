# Copyright (c) 2023, nts Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import nts

from prodman import get_default_company


def execute():
	company = get_default_company()
	if company:
		for d in nts.get_all("Lower Deduction Certificate", pluck="name"):
			nts.db.set_value("Lower Deduction Certificate", d, "company", company, update_modified=False)
