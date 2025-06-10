// Copyright (c) 2013, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Trial Balance for Party"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts .defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today()),
			reqd: 1,
			on_change: function (query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				nts .model.with_doc("Fiscal Year", fiscal_year, function (r) {
					var fy = nts .model.get_doc("Fiscal Year", fiscal_year);
					nts .query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date,
					});
				});
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today(), true)[2],
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "Party Type",
			default: "Customer",
			reqd: 1,
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				var party_type = nts .query_report.get_filter_value("party_type");
				var party = nts .query_report.get_filter_value("party");
				if (party && !party_type) {
					nts .throw(__("Please select Party Type first"));
				}
				return party_type;
			},
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
			fieldname: "show_zero_values",
			label: __("Show zero values"),
			fieldtype: "Check",
		},
	],
};
