// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
nts.query_reports["Campaign Efficiency"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[2],
		},
	],
};
