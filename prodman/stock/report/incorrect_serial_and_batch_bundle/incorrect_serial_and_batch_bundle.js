// Copyright (c) 2025, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Incorrect Serial and Batch Bundle"] = {
	filters: [
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
	],

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page.add_inner_button(__("Remove SABB Entry"), () => {
			let indexes = nts.query_report.datatable.rowmanager.getCheckedRows();
			let selected_rows = indexes.map((i) => nts.query_report.data[i]);

			if (!selected_rows.length) {
				nts.throw(__("Please select a row to create a Reposting Entry"));
			} else {
				nts.call({
					method: "prodman.stock.report.incorrect_serial_and_batch_bundle.incorrect_serial_and_batch_bundle.remove_sabb_entry",
					freeze: true,
					args: {
						selected_rows: selected_rows,
					},
					callback: function (r) {
						nts.query_report.refresh();
					},
				});
			}
		});
	},
};
