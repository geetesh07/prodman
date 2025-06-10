// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Electronic Invoice Register"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: nts.datetime.add_months(nts.datetime.get_today(), -1),
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts.datetime.get_today(),
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
		},
	],
	onload: function (reportview) {
		reportview.page.add_inner_button(__("Export E-Invoices"), function () {
			//TODO: refactor condition to disallow export if report has no data.
			if (!reportview.data.length) {
				nts.msgprint(__("No data to export"));
				return;
			}

			var w = window.open(
				nts.urllib.get_full_url(
					"/api/method/prodman.regional.italy.utils.export_invoices?" +
						"filters=" +
						JSON.stringify(reportview.get_filter_values())
				)
			);
			if (!w) {
				nts.msgprint(__("Please enable pop-ups"));
				return;
			}
		});
	},
};
