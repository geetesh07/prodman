// Copyright (c) 2018, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Global Defaults", {
	onload: function (frm) {
		frm.trigger("get_distance_uoms");
	},
	validate: function (frm) {
		frm.call("get_defaults", null, (r) => {
			nts.sys_defaults = r.message;
		});
	},
	get_distance_uoms: function (frm) {
		let units = [];

		nts.call({
			method: "nts.client.get_list",
			args: {
				doctype: "UOM Conversion Factor",
				filters: { category: __("Length") },
				fields: ["to_uom"],
				limit_page_length: 500,
			},
			callback: function (r) {
				r.message.forEach((row) => units.push(row.to_uom));
			},
		});
		frm.set_query("default_distance_unit", function () {
			return { filters: { name: ["IN", units] } };
		});
	},
});
