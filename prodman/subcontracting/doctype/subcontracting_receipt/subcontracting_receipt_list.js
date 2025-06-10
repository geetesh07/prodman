// Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.listview_settings["Subcontracting Receipt"] = {
	get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			Return: "gray",
			"Return Issued": "grey",
			Completed: "green",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
