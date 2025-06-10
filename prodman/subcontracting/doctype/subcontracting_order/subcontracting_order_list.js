// Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.listview_settings["Subcontracting Order"] = {
	get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			Open: "orange",
			"Partially Received": "yellow",
			Completed: "green",
			"Partial Material Transferred": "purple",
			"Material Transferred": "blue",
			Closed: "green",
			Cancelled: "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
