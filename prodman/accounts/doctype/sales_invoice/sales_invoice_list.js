// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
nts .listview_settings["Sales Invoice"] = {
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
		const status_colors = {
			Draft: "red",
			Unpaid: "orange",
			Paid: "green",
			Return: "gray",
			"Credit Note Issued": "gray",
			"Unpaid and Discounted": "orange",
			"Partly Paid and Discounted": "yellow",
			"Overdue and Discounted": "red",
			Overdue: "red",
			"Partly Paid": "yellow",
			"Internal Transfer": "darkgrey",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
	right_column: "grand_total",

	onload: function (listview) {
		if (nts .model.can_create("Delivery Note")) {
			listview.page.add_action_item(__("Delivery Note"), () => {
				prodman.bulk_transaction_processing.create(listview, "Sales Invoice", "Delivery Note");
			});
		}

		if (nts .model.can_create("Payment Entry")) {
			listview.page.add_action_item(__("Payment"), () => {
				prodman.bulk_transaction_processing.create(listview, "Sales Invoice", "Payment Entry");
			});
		}
	},
};
