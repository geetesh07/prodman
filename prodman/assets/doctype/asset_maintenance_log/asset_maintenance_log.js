// Copyright (c) 2017, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("Asset Maintenance Log", {
	asset_maintenance: (frm) => {
		frm.set_query("task", function (doc) {
			return {
				query: "prodman.assets.doctype.asset_maintenance_log.asset_maintenance_log.get_maintenance_tasks",
				filters: {
					asset_maintenance: doc.asset_maintenance,
				},
			};
		});
	},
});
