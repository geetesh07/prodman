# Copyright (c) 2013, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts  import _
from pypika import Order

from prodman.accounts.report.non_billed_report import get_ordered_to_be_billed_data


def execute(filters=None):
	columns = get_column()
	args = get_args()
	data = get_ordered_to_be_billed_data(args, filters)
	return columns, data


def get_column():
	return [
		{
			"label": _("Purchase Receipt"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 160,
		},
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 100},
		{
			"label": _("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 120,
		},
		{"label": _("Supplier Name"), "fieldname": "supplier_name", "fieldtype": "Data", "width": 120},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 100,
			"options": "Company:company:default_currency",
		},
		{
			"label": _("Billed Amount"),
			"fieldname": "billed_amount",
			"fieldtype": "Currency",
			"width": 100,
			"options": "Company:company:default_currency",
		},
		{
			"label": _("Returned Amount"),
			"fieldname": "returned_amount",
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"label": _("Pending Amount"),
			"fieldname": "pending_amount",
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 120},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 120},
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 120,
		},
	]


def get_args():
	return {
		"doctype": "Purchase Receipt",
		"party": "supplier",
		"date": "posting_date",
		"order": "name",
		"order_by": Order.desc,
		"reference_field": "purchase_receipt",
	}
