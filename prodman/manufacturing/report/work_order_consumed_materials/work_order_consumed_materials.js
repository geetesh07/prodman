// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Work Order Consumed Materials"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: nts.datetime.add_months(nts.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts.datetime.get_today(),
			reqd: 1,
		},
		{
			label: __("Work Order"),
			fieldname: "name",
			fieldtype: "Link",
			options: "Work Order",
			get_query: function () {
				return {
					filters: {
						status: ["in", ["In Process", "Completed", "Stopped"]],
					},
				};
			},
		},
		{
			label: __("Production Item"),
			fieldname: "production_item",
			fieldtype: "Link",
			depends_on: "eval: !doc.name",
			options: "Item",
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "In Process", "Completed", "Stopped"],
		},
		{
			label: __("Excess Materials Consumed"),
			fieldname: "show_extra_consumed_materials",
			fieldtype: "Check",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "raw_material_name" && data && data.extra_consumed_qty > 0) {
			value = `<div style="color:red">${value}</div>`;
		}

		return value;
	},
};
