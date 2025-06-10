// Copyright (c) 2017, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Manufacturer", {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			hide_field(["address_html", "contact_html"]);
			nts.contacts.clear_address_and_contact(frm);
		} else {
			unhide_field(["address_html", "contact_html"]);
			nts.contacts.render_address_and_contact(frm);
		}
	},
});
