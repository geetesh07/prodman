// Copyright (c) 2016, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Dimension-wise Accounts Balance Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts .defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today()),
			reqd: 1,
			on_change: function (query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				nts .model.with_doc("Fiscal Year", fiscal_year, function (r) {
					var fy = nts .model.get_doc("Fiscal Year", fiscal_year);
					nts .query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date,
					});
				});
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today(), true)[1],
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: prodman.utils.get_fiscal_year(nts .datetime.get_today(), true)[2],
			reqd: 1,
		},
		{
			fieldname: "finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book",
		},
		{
			fieldname: "dimension",
			label: __("Select Dimension"),
			fieldtype: "Select",
			default: "Cost Center",
			options: get_accounting_dimension_options(),
			reqd: 1,
		},
	],
	formatter: prodman.financial_statements.formatter,
	tree: true,
	name_field: "account",
	parent_field: "parent_account",
	initial_depth: 3,
};

function get_accounting_dimension_options() {
	let options = ["Cost Center", "Project"];
	nts .db.get_list("Accounting Dimension", { fields: ["document_type"] }).then((res) => {
		res.forEach((dimension) => {
			options.push(dimension.document_type);
		});
	});
	return options;
}
