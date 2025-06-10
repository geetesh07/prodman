# Copyright (c) 2013, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts

from prodman.projects.report.billing_summary import get_columns, get_data


def execute(filters=None):
	filters = nts._dict(filters or {})
	columns = get_columns()

	data = get_data(filters)
	return columns, data
