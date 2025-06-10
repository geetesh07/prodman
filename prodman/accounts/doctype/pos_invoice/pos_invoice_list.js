// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
nts .listview_settings["POS Invoice"] = {
	add_fields: [
		"customer",
		"customer_name",
		"base_grand_total",
		"outstanding_amount",
		"due_date",
		"company",
		"currency",
		"is_return",
	],
	get_indicator: function (doc) {
		var status_color = {
			Draft: "red",
			Unpaid: "orange",
			Paid: "green",
			Submitted: "blue",
			Consolidated: "green",
			Return: "darkgrey",
			"Unpaid and Discounted": "orange",
			"Overdue and Discounted": "red",
			Overdue: "red",
		};
		return [__(doc.status), status_color[doc.status], "status,=," + doc.status];
	},
	right_column: "grand_total",
	onload: function (me) {
		me.page.add_action_item("Make Merge Log", function () {
			const invoices = me.get_checked_items();
			nts .call({
				method: "prodman.accounts.doctype.pos_invoice.pos_invoice.make_merge_log",
				freeze: true,
				args: {
					invoices: invoices,
				},
				callback: function (r) {
					if (r.message) {
						var doc = nts .model.sync(r.message)[0];
						nts .set_route("Form", doc.doctype, doc.name);
					}
				},
			});
		});
	},
};
