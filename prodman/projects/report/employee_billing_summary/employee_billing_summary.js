// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Employee Billing Summary"] = {
	filters: [
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: nts.datetime.add_months(nts.datetime.month_start(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts.datetime.add_days(nts.datetime.month_start(), -1),
			reqd: 1,
		},
		{
			fieldname: "include_draft_timesheets",
			label: __("Include Timesheets in Draft Status"),
			fieldtype: "Check",
		},
	],
};
