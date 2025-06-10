// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Selling Settings", {
	after_save(frm) {
		nts.boot.user.defaults.editable_price_list_rate = frm.doc.editable_price_list_rate;
	},
});
