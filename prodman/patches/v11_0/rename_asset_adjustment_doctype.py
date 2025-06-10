# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.table_exists("Asset Adjustment") and not nts.db.table_exists("Asset Value Adjustment"):
		nts.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		nts.reload_doc("assets", "doctype", "asset_value_adjustment")
