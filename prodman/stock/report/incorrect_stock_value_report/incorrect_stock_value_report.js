// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Incorrect Stock Value Report"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: nts.defaults.get_user_default("Company"),
		},
		{
			label: __("Account"),
			fieldname: "account",
			fieldtype: "Link",
			options: "Account",
			get_query: function () {
				var company = nts.query_report.get_filter_value("company");
				return {
					filters: {
						account_type: "Stock",
						company: company,
					},
				};
			},
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
		},
	],
};
