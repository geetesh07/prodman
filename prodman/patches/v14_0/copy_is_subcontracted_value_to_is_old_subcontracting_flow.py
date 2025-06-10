# Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = nts.qb.DocType(doctype).as_("tab")
		nts.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(tab.is_subcontracted == 1).run()
