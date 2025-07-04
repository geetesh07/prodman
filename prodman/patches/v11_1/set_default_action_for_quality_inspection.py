# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	stock_settings = nts.get_doc("Stock Settings")
	if stock_settings.default_warehouse and not nts.db.exists(
		"Warehouse", stock_settings.default_warehouse
	):
		stock_settings.default_warehouse = None
	if stock_settings.stock_uom and not nts.db.exists("UOM", stock_settings.stock_uom):
		stock_settings.stock_uom = None
	stock_settings.flags.ignore_mandatory = True
	stock_settings.action_if_quality_inspection_is_not_submitted = "Stop"
	stock_settings.save()
