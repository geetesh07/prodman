# Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		nts.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null"""
		)
		nts.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'"""
		)

		nts.reload_doc(nts.get_meta(doctype).module, "doctype", nts.scrub(doctype))
