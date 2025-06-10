// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Item Shortage Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			width: "80",
			options: "Company",
			reqd: 1,
			default: nts.defaults.get_default("company"),
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "MultiSelectList",
			options: "Warehouse",
			width: "100",
			get_data: function (txt) {
				return nts.db.get_link_options("Warehouse", txt);
			},
		},
	],
};
