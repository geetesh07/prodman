// Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("POS Invoice Merge Log", {
	setup: function (frm) {
		frm.set_query("pos_invoice", "pos_invoices", (doc) => {
			return {
				filters: {
					docstatus: 1,
					customer: doc.customer,
					consolidated_invoice: "",
				},
			};
		});
	},

	merge_invoices_based_on: function (frm) {
		frm.set_value("customer", "");
		frm.set_value("customer_group", "");
	},
});
