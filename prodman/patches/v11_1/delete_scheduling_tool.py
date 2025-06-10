# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.exists("DocType", "Scheduling Tool"):
		nts.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
