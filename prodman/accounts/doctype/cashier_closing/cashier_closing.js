// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .ui.form.on("Cashier Closing", {
	setup: function (frm) {
		if (frm.doc.user == "" || frm.doc.user == null) {
			frm.doc.user = nts .session.user;
		}
	},
});
