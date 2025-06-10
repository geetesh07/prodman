// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Bin", {
	refresh(frm) {
		frm.trigger("recalculate_bin_quantity");
	},

	recalculate_bin_quantity(frm) {
		frm.add_custom_button(__("Recalculate Bin Qty"), () => {
			nts.call({
				method: "recalculate_qty",
				freeze: true,
				doc: frm.doc,
				callback: function (r) {
					nts.show_alert(__("Bin Qty Recalculated"), 2);
				},
			});
		});
	},
});
