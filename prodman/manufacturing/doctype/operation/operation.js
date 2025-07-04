// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Operation", {
	setup: function (frm) {
		frm.set_query("operation", "sub_operations", function () {
			return {
				filters: {
					name: ["not in", [frm.doc.name]],
				},
			};
		});
	},
});

nts.tour["Operation"] = [
	{
		fieldname: "__newname",
		title: "Operation Name",
		description: __("Enter a name for the Operation, for example, Cutting."),
	},
	{
		fieldname: "workstation",
		title: "Default Workstation",
		description: __(
			"Select the Default Workstation where the Operation will be performed. This will be fetched in BOMs and Work Orders."
		),
	},
	{
		fieldname: "sub_operations",
		title: "Sub Operations",
		description: __("If an operation is divided into sub operations, they can be added here."),
	},
];
