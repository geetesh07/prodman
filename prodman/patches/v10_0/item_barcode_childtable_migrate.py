# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("stock", "doctype", "item_barcode")
	if nts.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in nts.db.get_table_columns("Item"):
		return

	items_barcode = nts.db.sql("select name, barcode from tabItem where barcode is not null", as_dict=True)
	nts.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				nts.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (nts.DuplicateEntryError, nts.UniqueValidationError):
				continue
