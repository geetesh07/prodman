// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Incorrect Serial No Valuation"] = {
	filters: [
		{
			label: __("Item Code"),
			fieldtype: "Link",
			fieldname: "item_code",
			options: "Item",
			get_query: function () {
				return {
					filters: {
						has_serial_no: 1,
					},
				};
			},
		},
		{
			label: __("From Date"),
			fieldtype: "Date",
			fieldname: "from_date",
			reqd: 1,
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[1],
		},
		{
			label: __("To Date"),
			fieldtype: "Date",
			fieldname: "to_date",
			reqd: 1,
			default: prodman.utils.get_fiscal_year(nts.datetime.get_today(), true)[2],
		},
	],
};
