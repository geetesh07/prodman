// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Prospects Engaged But Not Converted"] = {
	filters: [
		{
			fieldname: "lead",
			label: __("Lead"),
			fieldtype: "Link",
			options: "Lead",
		},
		{
			fieldname: "no_of_interaction",
			label: __("Number of Interaction"),
			fieldtype: "Int",
			default: 1,
		},
		{
			fieldname: "lead_age",
			label: __("Minimum Lead Age (Days)"),
			fieldtype: "Int",
			default: 60,
		},
	],
};
