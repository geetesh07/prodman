// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Subcontract Order Summary"] = {
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
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: nts.datetime.add_months(nts.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: nts.datetime.get_today(),
			reqd: 1,
		},
		{
			label: __("Order Type"),
			fieldname: "order_type",
			fieldtype: "Select",
			options: ["Purchase Order", "Subcontracting Order"],
			default: "Subcontracting Order",
		},
		{
			label: __("Subcontract Order"),
			fieldname: "name",
			fieldtype: "Data",
		},
	],
};
