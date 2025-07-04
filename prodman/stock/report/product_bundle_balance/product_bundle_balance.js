// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt

nts.query_reports["Product Bundle Balance"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "date",
			label: __("Date"),
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
			get_query: function () {
				return {
					query: "prodman.controllers.queries.item_query",
					filters: { is_stock_item: 0 },
				};
			},
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			width: "80",
			options: "Item Group",
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			width: "80",
			options: "Warehouse",
		},
	],
	initial_depth: 0,
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data.parent_item) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
