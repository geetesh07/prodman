// Copyright (c) 2016, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Supplier Ledger Summary"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts .defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: nts .datetime.add_months(nts .datetime.get_today(), -1),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: nts .datetime.get_today(),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book",
		},
		{
			fieldname: "party",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			on_change: () => {
				var party = nts .query_report.get_filter_value("party");
				if (party) {
					nts .db.get_value("Supplier", party, ["tax_id", "supplier_name"], function (value) {
						nts .query_report.set_filter_value("tax_id", value["tax_id"]);
						nts .query_report.set_filter_value("supplier_name", value["supplier_name"]);
					});
				} else {
					nts .query_report.set_filter_value("tax_id", "");
					nts .query_report.set_filter_value("supplier_name", "");
				}
			},
		},
		{
			fieldname: "supplier_group",
			label: __("Supplier Group"),
			fieldtype: "Link",
			options: "Supplier Group",
		},
		{
			fieldname: "payment_terms_template",
			label: __("Payment Terms Template"),
			fieldtype: "Link",
			options: "Payment Terms Template",
		},
		{
			fieldname: "tax_id",
			label: __("Tax Id"),
			fieldtype: "Data",
			hidden: 1,
		},
		{
			fieldname: "supplier_name",
			label: __("Supplier Name"),
			fieldtype: "Data",
			hidden: 1,
		},
	],
};
