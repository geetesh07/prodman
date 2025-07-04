// Copyright (c) 2017, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Driver", {
	setup: function (frm) {
		frm.set_query("transporter", function () {
			return {
				filters: {
					is_transporter: 1,
				},
			};
		});
	},

	refresh: function (frm) {
		frm.set_query("address", function () {
			return {
				filters: {
					is_your_company_address: !frm.doc.transporter ? 1 : 0,
				},
			};
		});
	},

	transporter: function (frm, cdt, cdn) {
		// this assumes that supplier's address has same title as supplier's name
		nts.db
			.get_doc("Address", null, { address_title: frm.doc.transporter })
			.then((r) => {
				nts.model.set_value(cdt, cdn, "address", r.name);
			})
			.catch((err) => {
				console.log(err);
			});
	},
});
