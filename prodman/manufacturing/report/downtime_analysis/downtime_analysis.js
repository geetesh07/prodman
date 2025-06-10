// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Downtime Analysis"] = {
	filters: [
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Datetime",
			default: nts.datetime.convert_to_system_tz(
				nts.datetime.add_months(nts.datetime.now_datetime(), -1)
			),
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Datetime",
			default: nts.datetime.now_datetime(),
			reqd: 1,
		},
		{
			label: __("Machine"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation",
		},
	],
};
