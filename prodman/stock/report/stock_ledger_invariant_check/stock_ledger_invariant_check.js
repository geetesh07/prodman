// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

const DIFFERENCE_FIELD_NAMES = [
	"difference_in_qty",
	"fifo_qty_diff",
	"fifo_value_diff",
	"fifo_valuation_diff",
	"valuation_diff",
	"fifo_difference_diff",
	"diff_value_diff",
];

nts.query_reports["Stock Ledger Invariant Check"] = {
	filters: [
		{
			fieldname: "item_code",
			fieldtype: "Link",
			label: "Item",
			mandatory: 1,
			options: "Item",
			get_query: function () {
				return {
					filters: { is_stock_item: 1, has_serial_no: 0 },
				};
			},
		},
		{
			fieldname: "warehouse",
			fieldtype: "Link",
			label: "Warehouse",
			mandatory: 1,
			options: "Warehouse",
		},
		{
			fieldname: "show_incorrect_entries",
			fieldtype: "Check",
			label: "Show Incorrect Entries",
			default: 0,
		},
	],

	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (DIFFERENCE_FIELD_NAMES.includes(column.fieldname) && Math.abs(data[column.fieldname]) > 0.001) {
			value = '<span style="color:red">' + value + "</span>";
		}
		return value;
	},

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page.add_inner_button(__("Create Reposting Entry"), () => {
			let message = `
				<div>
					<p>
						Reposting Entry will change the value of
						accounts Stock In Hand, and Stock Expenses
						in the Trial Balance report and will also change
						the Balance Value in the Stock Balance report.
					</p>
					<p>Are you sure you want to create a Reposting Entry?</p>
				</div>`;
			let indexes = nts.query_report.datatable.rowmanager.getCheckedRows();
			let selected_rows = indexes.map((i) => nts.query_report.data[i]);

			if (!selected_rows.length) {
				nts.throw(__("Please select a row to create a Reposting Entry"));
			} else if (selected_rows.length > 1) {
				nts.throw(__("Please select only one row to create a Reposting Entry"));
			} else {
				nts.confirm(__(message), () => {
					nts.call({
						method: "prodman.stock.report.stock_ledger_invariant_check.stock_ledger_invariant_check.create_reposting_entries",
						args: {
							rows: selected_rows,
							item_code: nts.query_report.get_filter_values().item_code,
							warehouse: nts.query_report.get_filter_values().warehouse,
						},
					});
				});
			}
		});
	},
};
