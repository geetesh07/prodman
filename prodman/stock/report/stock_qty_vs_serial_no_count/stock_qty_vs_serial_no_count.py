# Copyright (c) 2013, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _


def execute(filters=None):
	validate_warehouse(filters)
	columns = get_columns()
	data = get_data(filters.warehouse)
	return columns, data


def validate_warehouse(filters):
	company = filters.company
	warehouse = filters.warehouse
	if not nts.db.exists("Warehouse", {"name": warehouse, "company": company}):
		nts.throw(_("Warehouse: {0} does not belong to {1}").format(warehouse, company))


def get_columns():
	columns = [
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": _("Serial No Count"), "fieldname": "total", "fieldtype": "Float", "width": 150},
		{"label": _("Stock Qty"), "fieldname": "stock_qty", "fieldtype": "Float", "width": 150},
		{"label": _("Difference"), "fieldname": "difference", "fieldtype": "Float", "width": 150},
	]

	return columns


def get_data(warehouse):
	serial_item_list = nts.get_all(
		"Item",
		filters={
			"has_serial_no": True,
		},
		fields=["item_code", "item_name"],
	)

	status_list = ["Active", "Expired"]
	data = []
	for item in serial_item_list:
		total_serial_no = nts.db.count(
			"Serial No",
			filters={"item_code": item.item_code, "status": ("in", status_list), "warehouse": warehouse},
		)

		actual_qty = nts.db.get_value(
			"Bin", fieldname=["actual_qty"], filters={"warehouse": warehouse, "item_code": item.item_code}
		)

		# nts.db.get_value returns null if no record exist.
		if not actual_qty:
			actual_qty = 0

		difference = total_serial_no - actual_qty

		row = {
			"item_code": item.item_code,
			"item_name": item.item_name,
			"total": total_serial_no,
			"stock_qty": actual_qty,
			"difference": difference,
		}

		data.append(row)

	return data
