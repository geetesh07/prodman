// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Territory-wise Sales"] = {
	breadcrumb: "Selling",
	filters: [
		{
			fieldname: "transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [
				nts.datetime.add_months(nts.datetime.get_today(), -1),
				nts.datetime.get_today(),
			],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		},
	],
};
