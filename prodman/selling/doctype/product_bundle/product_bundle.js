// Copyright (c) 2021, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Product Bundle", {
	refresh: function (frm) {
		frm.toggle_enable("new_item_code", frm.is_new());
		frm.set_query("new_item_code", () => {
			return {
				query: "prodman.selling.doctype.product_bundle.product_bundle.get_new_item_code",
			};
		});

		frm.set_query("item_code", "items", () => {
			return {
				filters: {
					has_variants: 0,
				},
			};
		});
	},
});
