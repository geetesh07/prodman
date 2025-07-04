// Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Warehouse Wise Stock Balance"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: nts.defaults.get_user_default("Company"),
		},
		{
			fieldname: "show_disabled_warehouses",
			label: __("Show Disabled Warehouses"),
			fieldtype: "Check",
			default: 0,
		},
	],
	initial_depth: 3,
	tree: true,
	parent_field: "parent_warehouse",
	name_field: "warehouse",
};
