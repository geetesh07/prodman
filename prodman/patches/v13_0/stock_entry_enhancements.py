# Copyright(c) 2020, nts Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import nts


def execute():
	nts.reload_doc("stock", "doctype", "stock_entry")
	if nts.db.has_column("Stock Entry", "add_to_transit"):
		nts.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		nts.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		nts.reload_doc("stock", "doctype", "warehouse_type")
		if not nts.db.exists("Warehouse Type", "Transit"):
			doc = nts.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		nts.reload_doc("stock", "doctype", "stock_entry_type")
		nts.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		nts.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
