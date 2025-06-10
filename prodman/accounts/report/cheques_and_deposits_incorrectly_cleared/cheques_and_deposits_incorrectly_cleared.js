// Copyright (c) 2024, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Cheques and Deposits Incorrectly cleared"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: nts .defaults.get_user_default("Company"),
		},
		{
			fieldname: "account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Account",
			default: nts .defaults.get_user_default("Company")
				? locals[":Company"][nts .defaults.get_user_default("Company")]["default_bank_account"]
				: "",
			reqd: 1,
			get_query: function () {
				var company = nts .query_report.get_filter_value("company");
				return {
					query: "prodman.controllers.queries.get_account_list",
					filters: [
						["Account", "account_type", "in", "Bank, Cash"],
						["Account", "is_group", "=", 0],
						["Account", "disabled", "=", 0],
						["Account", "company", "=", company],
					],
				};
			},
		},
		{
			fieldname: "report_date",
			label: __("Date"),
			fieldtype: "Date",
			default: nts .datetime.get_today(),
			reqd: 1,
		},
	],
};
