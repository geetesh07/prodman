// Copyright (c) 2022, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
nts .provide("prodman.asset");

nts .ui.form.on("Asset Depreciation Schedule", {
	onload: function (frm) {
		frm.events.make_schedules_editable(frm);
	},

	make_schedules_editable: function (frm) {
		var is_manual_hence_editable = frm.doc.depreciation_method === "Manual" ? true : false;
		var is_shift_hence_editable = frm.doc.shift_based ? true : false;

		frm.toggle_enable("depreciation_schedule", is_manual_hence_editable || is_shift_hence_editable);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable(
			"schedule_date",
			is_manual_hence_editable
		);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable(
			"depreciation_amount",
			is_manual_hence_editable
		);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable("shift", is_shift_hence_editable);
	},
});

nts .ui.form.on("Depreciation Schedule", {
	make_depreciation_entry: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (!row.journal_entry) {
			nts .call({
				method: "prodman.assets.doctype.asset.depreciation.make_depreciation_entry",
				args: {
					asset_depr_schedule_name: frm.doc.name,
					date: row.schedule_date,
				},
				debounce: 1000,
				callback: function (r) {
					nts .model.sync(r.message);
					frm.refresh();
				},
			});
		}
	},

	depreciation_amount: function (frm, cdt, cdn) {
		prodman.asset.set_accumulated_depreciation(frm);
	},
});

prodman.asset.set_accumulated_depreciation = function (frm) {
	if (frm.doc.depreciation_method != "Manual") return;

	var accumulated_depreciation = flt(frm.doc.opening_accumulated_depreciation);

	$.each(frm.doc.depreciation_schedule || [], function (i, row) {
		accumulated_depreciation += flt(row.depreciation_amount);
		nts .model.set_value(
			row.doctype,
			row.name,
			"accumulated_depreciation_amount",
			accumulated_depreciation
		);
	});
};
