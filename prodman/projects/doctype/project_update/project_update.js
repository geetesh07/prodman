// Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Project Update", {
	refresh: function () {},

	onload: function (frm) {
		frm.set_value("naming_series", "UPDATE-.project.-.YY.MM.DD.-.####");
	},

	validate: function (frm) {
		frm.set_value("time", nts.datetime.now_time());
		frm.set_value("date", nts.datetime.nowdate());
	},
});
