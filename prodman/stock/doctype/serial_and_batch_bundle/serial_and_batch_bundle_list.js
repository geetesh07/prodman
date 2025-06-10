// Copyright (c) 2023, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.listview_settings["Serial and Batch Bundle"] = {
	add_fields: ["is_cancelled"],
	get_indicator: function (doc) {
		if (doc.is_cancelled) {
			return [__("Cancelled"), "red", "is_cancelled,=,1"];
		}
	},
};
