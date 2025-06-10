// Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Campaign", {
	refresh: function (frm) {
		prodman.toggle_naming_series();

		if (frm.is_new()) {
			frm.toggle_display(
				"naming_series",
				nts.boot.sysdefaults.campaign_naming_by == "Naming Series"
			);
		} else {
			cur_frm.add_custom_button(
				__("View Leads"),
				function () {
					nts.route_options = { source: "Campaign", campaign_name: frm.doc.name };
					nts.set_route("List", "Lead");
				},
				"fa fa-list",
				true
			);
		}
	},
});
