// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .query_reports["Bank Reconciliation Statement"] = {
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
		{
			fieldname: "include_pos_transactions",
			label: __("Include POS Transactions"),
			fieldtype: "Check",
		},
	],
	formatter: function (value, row, column, data, default_formatter, filter) {
		if (column.fieldname == "payment_entry" && value == __("Cheques and Deposits incorrectly cleared")) {
			column.link_onclick =
				"nts .query_reports['Bank Reconciliation Statement'].open_utility_report()";
		}
		return default_formatter(value, row, column, data);
	},
	open_utility_report: function () {
		nts .route_options = {
			company: nts .query_report.get_filter_value("company"),
			account: nts .query_report.get_filter_value("account"),
			report_date: nts .query_report.get_filter_value("report_date"),
		};
		nts .open_in_new_tab = true;
		nts .set_route("query-report", "Cheques and Deposits Incorrectly cleared");
	},
};
