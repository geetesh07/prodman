// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Job Card Summary"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today()),
			reqd: 1,
			on_change: function (query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				nts.model.with_doc("Fiscal Year", fiscal_year, function (r) {
					var fy = nts.model.get_doc("Fiscal Year", fiscal_year);
					nts.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date,
					});
				});
			},
		},
		{
			label: __("From Posting Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[1],
			reqd: 1,
		},
		{
			label: __("To Posting Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[2],
			reqd: 1,
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "Open", "Work In Progress", "Completed", "On Hold"],
		},
		{
			label: __("Work Orders"),
			fieldname: "work_order",
			fieldtype: "MultiSelectList",
			options: "Work Order",
			get_data: function (txt) {
				return nts.db.get_link_options("Work Order", txt);
			},
		},
		{
			label: __("Production Item"),
			fieldname: "production_item",
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function (txt) {
				return nts.db.get_link_options("Item", txt);
			},
		},
		{
			label: __("Workstation"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation",
		},
		{
			label: __("Operation"),
			fieldname: "operation",
			fieldtype: "Link",
			options: "Operation",
		},
	],
};
