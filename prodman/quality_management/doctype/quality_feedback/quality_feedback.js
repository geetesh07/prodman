// Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Quality Feedback", {
	template: function (frm) {
		if (frm.doc.template) {
			frm.call("set_parameters");
		}
	},
});
