# Copyright (c) 2013, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import defaultdict

import nts
from nts import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_data(report_filters):
	fields = get_fields()
	filters = get_filter_condition(report_filters)

	wo_items = {}

	work_orders = nts.get_all("Work Order", filters=filters, fields=fields)
	get_returned_materials(work_orders)

	for d in work_orders:
		d.extra_consumed_qty = 0.0
		if d.consumed_qty and d.consumed_qty > d.required_qty:
			d.extra_consumed_qty = d.consumed_qty - d.required_qty

		if d.extra_consumed_qty or not report_filters.show_extra_consumed_materials:
			wo_items.setdefault((d.name, d.production_item), []).append(d)

	data = []
	for _key, wo_data in wo_items.items():
		for index, row in enumerate(wo_data):
			if index != 0:
				# If one work order has multiple raw materials then show parent data in the first row only
				for field in ["name", "status", "production_item", "qty", "produced_qty"]:
					row[field] = ""

			data.append(row)

	return data


def get_returned_materials(work_orders):
	raw_materials_qty = defaultdict(float)

	raw_materials = nts.get_all(
		"Stock Entry",
		fields=[
			"`tabStock Entry`.`work_order`",
			"`tabStock Entry Detail`.`item_code`",
			"`tabStock Entry Detail`.`qty`",
		],
		filters=[
			["Stock Entry", "is_return", "=", 1],
			["Stock Entry Detail", "docstatus", "=", 1],
			["Stock Entry", "work_order", "in", [d.name for d in work_orders]],
		],
	)

	for d in raw_materials:
		key = (d.work_order, d.item_code)
		raw_materials_qty[key] += d.qty

	for row in work_orders:
		row.returned_qty = 0.0
		key = (row.parent, row.raw_material_item_code)
		if raw_materials_qty.get(key):
			row.returned_qty = raw_materials_qty.get(key)


def get_fields():
	return [
		"`tabWork Order Item`.`parent`",
		"`tabWork Order Item`.`item_code` as raw_material_item_code",
		"`tabWork Order Item`.`item_name` as raw_material_name",
		"`tabWork Order Item`.`required_qty`",
		"`tabWork Order Item`.`transferred_qty`",
		"`tabWork Order Item`.`consumed_qty`",
		"`tabWork Order`.`status`",
		"`tabWork Order`.`name`",
		"`tabWork Order`.`production_item`",
		"`tabWork Order`.`qty`",
		"`tabWork Order`.`produced_qty`",
	]


def get_filter_condition(report_filters):
	filters = {
		"docstatus": 1,
		"status": ("in", ["In Process", "Completed", "Stopped"]),
		"creation": ("between", [report_filters.from_date, report_filters.to_date]),
	}

	for field in ["name", "production_item", "company", "status"]:
		value = report_filters.get(field)
		if value:
			key = f"{field}"
			filters.update({key: value})

	return filters


def get_columns():
	return [
		{
			"label": _("Id"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Work Order",
			"width": 80,
		},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 80},
		{
			"label": _("Production Item"),
			"fieldname": "production_item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 130,
		},
		{"label": _("Qty to Produce"), "fieldname": "qty", "fieldtype": "Float", "width": 120},
		{"label": _("Produced Qty"), "fieldname": "produced_qty", "fieldtype": "Float", "width": 110},
		{
			"label": _("Raw Material Item"),
			"fieldname": "raw_material_item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{"label": _("Item Name"), "fieldname": "raw_material_name", "width": 130},
		{"label": _("Required Qty"), "fieldname": "required_qty", "fieldtype": "Float", "width": 100},
		{
			"label": _("Transferred Qty"),
			"fieldname": "transferred_qty",
			"fieldtype": "Float",
			"width": 100,
		},
		{"label": _("Consumed Qty"), "fieldname": "consumed_qty", "fieldtype": "Float", "width": 100},
		{
			"label": _("Extra Consumed Qty"),
			"fieldname": "extra_consumed_qty",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Returned Qty"),
			"fieldname": "returned_qty",
			"fieldtype": "Float",
			"width": 100,
		},
	]
