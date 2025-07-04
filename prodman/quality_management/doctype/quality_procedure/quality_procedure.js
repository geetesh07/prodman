// Copyright (c) 2018, nts and contributors
// For license information, please see license.txt

nts.ui.form.on("Quality Procedure", {
	refresh: function (frm) {
		frm.set_query("procedure", "processes", (frm) => {
			return {
				filters: {
					name: ["not in", [frm.parent_quality_procedure, frm.name]],
				},
			};
		});

		frm.set_query("parent_quality_procedure", function () {
			return {
				filters: {
					is_group: 1,
					name: ["!=", frm.doc.name],
				},
			};
		});
	},
});
