// Copyright (c) 2022, nts  Technologies Pvt. Ltd. and contributors
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
				});
			},
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "Party Type",
			default: "",
			on_change: function () {
				nts .query_report.set_filter_value("party", "");
			},
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "MultiSelectList",
			options: "party_type",
			get_data: function (txt) {
				if (!nts .query_report.filters) return;

				let party_type = nts .query_report.get_filter_value("party_type");
				if (!party_type) return;

				return nts .db.get_link_options(party_type, txt);
			},
		},
		{
			fieldname: "voucher_no",
			label: __("Voucher No"),
			fieldtype: "Data",
			width: 100,
		},
		{
			fieldname: "against_voucher_no",
			label: __("Against Voucher No"),
			fieldtype: "Data",
			width: 100,
		},
		{
			fieldname: "include_account_currency",
			label: __("Include Account Currency"),
			fieldtype: "Check",
			width: 100,
		},
		{
			fieldname: "group_party",
			label: __("Group by Party"),
			fieldtype: "Check",
			width: 100,
		},
	];
	return filters;
}

nts .query_reports["Payment Ledger"] = {
	filters: get_filters(),
};
