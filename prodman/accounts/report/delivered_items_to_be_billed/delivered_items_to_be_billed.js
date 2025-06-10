// Copyright (c) 2016, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Delivered Items To Be Billed"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: nts .defaults.get_default("Company"),
		},
		{
			label: __("As on Date"),
			fieldname: "posting_date",
			fieldtype: "Date",
			reqd: 1,
			default: nts .datetime.get_today(),
		},
		{
			label: __("Delivery Note"),
			fieldname: "delivery_note",
			fieldtype: "Link",
			options: "Delivery Note",
		},
	],
};
