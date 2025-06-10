# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if nts.db.exists("Report", report):
			nts.delete_doc("Report", report)
