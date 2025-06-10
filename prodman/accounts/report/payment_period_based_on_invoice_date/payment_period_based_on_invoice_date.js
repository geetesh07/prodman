// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .query_reports["Payment Period Based On Invoice Date"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: nts .defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts .datetime.get_today(),
		},
		{
			fieldname: "payment_type",
			label: __("Payment Type"),
			fieldtype: "Select",
			options: __("Incoming") + "\n" + __("Outgoing"),
			default: __("Incoming"),
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "DocType",
			get_query: function () {
				return {
					filters: { name: ["in", ["Customer", "Supplier"]] },
				};
			},
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				var party_type = nts .query_report.get_filter_value("party_type");
				var party = nts .query_report.get_filter_value("party");
				if (party && !party_type) {
					nts .throw(__("Please select Party Type first"));
				}
				return party_type;
			},
		},
	],
};
