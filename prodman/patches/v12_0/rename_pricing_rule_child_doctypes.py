# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not nts.db.table_exists(new_doc) and nts.db.table_exists(old_doc):
			nts.rename_doc("DocType", old_doc, new_doc)
			nts.reload_doc("accounts", "doctype", nts.scrub(new_doc))
			nts.delete_doc("DocType", old_doc)
