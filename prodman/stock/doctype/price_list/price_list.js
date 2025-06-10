// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Price List", {
	refresh: function (frm) {
		let me = this;
		frm.add_custom_button(
			__("Add / Edit Prices"),
			function () {
				nts.route_options = {
					price_list: frm.doc.name,
				};
				nts.set_route("Report", "Item Price");
			},
			"fa fa-money"
		);
	},
});
