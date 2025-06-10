// Copyright (c) 2016, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Received Items To Be Billed"] = {
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
			label: __("Purchase Receipt"),
			fieldname: "purchase_receipt",
			fieldtype: "Link",
			options: "Purchase Receipt",
		},
	],
};
