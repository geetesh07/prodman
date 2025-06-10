# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("assets", "doctype", "Location")
	for dt in (
		"Account",
		"Cost Center",
		"File",
		"Employee",
		"Location",
		"Task",
		"Customer Group",
		"Sales Person",
		"Territory",
	):
		nts.reload_doctype(dt)
		nts.get_doc("DocType", dt).run_module_method("on_doctype_update")
