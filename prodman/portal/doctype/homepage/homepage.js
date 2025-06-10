// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Homepage", {
	refresh: function (frm) {
		frm.add_custom_button(__("Set Meta Tags"), () => {
			nts.utils.set_meta_tag("home");
		});
		frm.add_custom_button(__("Customize Homepage Sections"), () => {
			nts.set_route("List", "Homepage Section", "List");
		});
	},
});
