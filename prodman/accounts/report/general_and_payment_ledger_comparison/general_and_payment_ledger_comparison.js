// Copyright (c) 2023, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

function get_filters() {
	let filters = [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts .defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "period_start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			reqd: 1,
			default: nts .datetime.add_months(nts .datetime.get_today(), -1),
		},
		{
			fieldname: "period_end_date",
			label: __("End Date"),
			fieldtype: "Date",
			reqd: 1,
			default: nts .datetime.get_today(),
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "MultiSelectList",
			options: "Account",
			get_data: function (txt) {
				return nts .db.get_link_options("Account", txt, {
					company: nts .query_report.get_filter_value("company"),
					account_type: ["in", ["Receivable", "Payable"]],
				});
			},
		},
		{
			fieldname: "voucher_no",
			label: __("Voucher No"),
			fieldtype: "Data",
			width: 100,
		},
	];
	return filters;
}

nts .query_reports["General and Payment Ledger Comparison"] = {
	filters: get_filters(),
};
