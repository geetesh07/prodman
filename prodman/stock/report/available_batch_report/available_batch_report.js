// Copyright (c) 2024, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Available Batch Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			width: "80",
			options: "Company",
			default: nts.defaults.get_default("company"),
		},
		{
			fieldname: "to_date",
			label: __("On This Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: nts.datetime.get_today(),
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			width: "80",
			options: "Item",
			get_query: () => {
				return {
					filters: {
						has_batch_no: 1,
						disabled: 0,
					},
				};
			},
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			width: "80",
			options: "Warehouse",
			get_query: () => {
				let warehouse_type = nts.query_report.get_filter_value("warehouse_type");
				let company = nts.query_report.get_filter_value("company");

				return {
					filters: {
						...(warehouse_type && { warehouse_type }),
						...(company && { company }),
					},
				};
			},
		},
		{
			fieldname: "warehouse_type",
			label: __("Warehouse Type"),
			fieldtype: "Link",
			width: "80",
			options: "Warehouse Type",
		},
		{
			fieldname: "batch_no",
			label: __("Batch No"),
			fieldtype: "Link",
			width: "80",
			options: "Batch",
			get_query: () => {
				let item = nts.query_report.get_filter_value("item_code");

				return {
					filters: {
						...(item && { item }),
					},
				};
			},
		},
		{
			fieldname: "include_expired_batches",
			label: __("Include Expired Batches"),
			fieldtype: "Check",
			width: "80",
		},
		{
			fieldname: "show_item_name",
			label: __("Show Item Name"),
			fieldtype: "Check",
			width: "80",
		},
	],
};
