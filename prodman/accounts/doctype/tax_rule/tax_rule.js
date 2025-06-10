// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .ui.form.on("Tax Rule", "customer", function (frm) {
	if (frm.doc.customer) {
		nts .call({
			method: "prodman.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				party: frm.doc.customer,
				party_type: "customer",
			},
			callback: function (r) {
				if (!r.exc) {
					$.each(r.message, function (k, v) {
						frm.set_value(k, v);
					});
				}
			},
		});
	}
});

nts .ui.form.on("Tax Rule", "supplier", function (frm) {
	if (frm.doc.supplier) {
		nts .call({
			method: "prodman.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				party: frm.doc.supplier,
				party_type: "supplier",
			},
			callback: function (r) {
				if (!r.exc) {
					$.each(r.message, function (k, v) {
						frm.set_value(k, v);
					});
				}
			},
		});
	}
});
