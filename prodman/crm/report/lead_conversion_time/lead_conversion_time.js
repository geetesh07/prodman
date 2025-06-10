// Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Lead Conversion Time"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: nts.datetime.add_days(nts.datetime.nowdate(), -30),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: nts.datetime.nowdate(),
		},
	],
};
