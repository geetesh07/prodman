// Copyright (c) 2023, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.listview_settings["Pick List"] = {
	get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			Open: "orange",
			Completed: "green",
			Cancelled: "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
