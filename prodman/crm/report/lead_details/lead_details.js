// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Lead Details"] = {
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
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: nts.datetime.add_months(nts.datetime.get_today(), -12),
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
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: [
				{ value: "Lead", label: __("Lead") },
				{ value: "Open", label: __("Open") },
				{ value: "Replied", label: __("Replied") },
				{ value: "Opportunity", label: __("Opportunity") },
				{ value: "Quotation", label: __("Quotation") },
				{ value: "Lost Quotation", label: __("Lost Quotation") },
				{ value: "Interested", label: __("Interested") },
				{ value: "Converted", label: __("Converted") },
				{ value: "Do Not Contact", label: __("Do Not Contact") },
			],
		},
		{
			fieldname: "territory",
			label: __("Territory"),
			fieldtype: "Link",
			options: "Territory",
		},
	],
};
