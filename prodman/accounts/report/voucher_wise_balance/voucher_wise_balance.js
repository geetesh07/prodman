// Copyright (c) 2023, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Voucher-wise Balance"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: nts .datetime.add_months(nts .datetime.get_today(), -1),
			width: "60px",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts .datetime.get_today(),
			width: "60px",
		},
	],
};
