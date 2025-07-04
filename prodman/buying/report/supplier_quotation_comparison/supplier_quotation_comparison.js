// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.query_reports["Supplier Quotation Comparison"] = {
	filters: [
		{
			fieldtype: "Link",
			label: __("Company"),
			options: "Company",
			fieldname: "company",
			default: nts.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: nts.datetime.add_months(nts.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: nts.datetime.get_today(),
		},
		{
			default: "",
			options: "Item",
			label: __("Item"),
			fieldname: "item_code",
			fieldtype: "Link",
			get_query: () => {
				let quote = nts.query_report.get_filter_value("supplier_quotation");
				if (quote != "") {
					return {
						query: "prodman.stock.doctype.quality_inspection.quality_inspection.item_query",
						filters: {
							from: "Supplier Quotation Item",
							parent: quote,
						},
					};
				}
			},
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "MultiSelectList",
			options: "Supplier",
			get_data: function (txt) {
				return nts.db.get_link_options("Supplier", txt);
			},
		},
		{
			fieldtype: "MultiSelectList",
			label: __("Supplier Quotation"),
			fieldname: "supplier_quotation",
			options: "Supplier Quotation",
			default: "",
			get_data: function (txt) {
				return nts.db.get_link_options("Supplier Quotation", txt, { docstatus: ["<", 2] });
			},
		},
		{
			fieldtype: "Link",
			label: __("Request for Quotation"),
			options: "Request for Quotation",
			fieldname: "request_for_quotation",
			default: "",
			get_query: () => {
				return { filters: { docstatus: ["<", 2] } };
			},
		},
		{
			fieldname: "categorize_by",
			label: __("Categorize by"),
			fieldtype: "Select",
			options: [
				{ label: __("Categorize by Supplier"), value: "Categorize by Supplier" },
				{ label: __("Categorize by Item"), value: "Categorize by Item" },
			],
			default: __("Categorize by Supplier"),
		},
		{
			fieldtype: "Check",
			label: __("Include Expired"),
			fieldname: "include_expired",
			default: 0,
		},
	],

	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "valid_till" && data.valid_till) {
			if (nts.datetime.get_diff(data.valid_till, nts.datetime.nowdate()) <= 1) {
				value = `<div style="color:red">${value}</div>`;
			} else if (nts.datetime.get_diff(data.valid_till, nts.datetime.nowdate()) <= 7) {
				value = `<div style="color:darkorange">${value}</div>`;
			}
		}

		if (column.fieldname === "price_per_unit" && data.price_per_unit && data.min && data.min === 1) {
			value = `<div style="color:green">${value}</div>`;
		}
		return value;
	},

	onload: (report) => {
		// Create a button for setting the default supplier
		report.page.add_inner_button(
			__("Select Default Supplier"),
			() => {
				let reporter = nts.query_reports["Supplier Quotation Comparison"];

				//Always make a new one so that the latest values get updated
				reporter.make_default_supplier_dialog(report);
			},
			__("Tools")
		);
	},
	make_default_supplier_dialog: (report) => {
		// Get the name of the item to change
		if (!report.data) return;

		let filters = report.get_values();
		let item_code = filters.item_code;

		// Get a list of the suppliers (with a blank as well) for the user to select
		let suppliers = $.map(report.data, (row, idx) => {
			return row.supplier_name;
		});

		let items = [];
		report.data.forEach((d) => {
			if (!items.includes(d.item_code)) {
				items.push(d.item_code);
			}
		});

		// Create a dialog window for the user to pick their supplier
		let dialog = new nts.ui.Dialog({
			title: __("Select Default Supplier"),
			fields: [
				{
					reqd: 1,
					label: "Supplier",
					fieldtype: "Link",
					options: "Supplier",
					fieldname: "supplier",
					get_query: () => {
						return {
							filters: {
								name: ["in", suppliers],
							},
						};
					},
				},
				{
					reqd: 1,
					label: "Item",
					fieldtype: "Link",
					options: "Item",
					fieldname: "item_code",
					get_query: () => {
						return {
							filters: {
								name: ["in", items],
							},
						};
					},
				},
			],
		});

		dialog.set_primary_action(__("Set Default Supplier"), () => {
			let values = dialog.get_values();

			if (values) {
				// Set the default_supplier field of the appropriate Item to the selected supplier
				nts.call({
					method: "prodman.buying.report.supplier_quotation_comparison.supplier_quotation_comparison.set_default_supplier",
					args: {
						item_code: values.item_code,
						supplier: values.supplier,
						company: filters.company,
					},
					freeze: true,
					callback: (r) => {
						nts.msgprint(__("Successfully Set Supplier"));
						dialog.hide();
					},
				});
			}
		});
		dialog.show();
	},
};
