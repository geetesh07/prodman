// Copyright (c) 2018, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .listview_settings["Bank Transaction"] = {
	add_fields: ["unallocated_amount"],
	get_indicator: function (doc) {
		if (doc.docstatus == 2) {
			return [__("Cancelled"), "red", "docstatus,=,2"];
		} else if (flt(doc.unallocated_amount) <= 0) {
			return [__("Reconciled"), "green", "unallocated_amount,=,0"];
		} else if (flt(doc.unallocated_amount) > 0) {
			return [__("Unreconciled"), "orange", "unallocated_amount,>,0"];
		}
	},
};
