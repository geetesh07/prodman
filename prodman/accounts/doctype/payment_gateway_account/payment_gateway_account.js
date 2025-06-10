// Copyright (c) 2019, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .ui.form.on("Payment Gateway Account", {
	refresh(frm) {
		prodman.utils.check_payments_app();
		if (!frm.doc.__islocal) {
			frm.set_df_property("payment_gateway", "read_only", 1);
		}
	},
});
