// Copyright (c) 2024, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Code List", {
	refresh: (frm) => {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Import Genericode File"), function () {
				prodman.edi.import_genericode(frm);
			});
		}
	},
	setup: (frm) => {
		frm.savetrash = () => {
			frm.validate_form_action("Delete");
			nts.confirm(
				__(
					"Are you sure you want to delete {0}?<p>This action will also delete all associated Common Code documents.</p>",
					[frm.docname.bold()]
				),
				function () {
					return nts.call({
						method: "nts.client.delete",
						args: {
							doctype: frm.doctype,
							name: frm.docname,
						},
						freeze: true,
						freeze_message: __("Deleting {0} and all associated Common Code documents...", [
							frm.docname,
						]),
						callback: function (r) {
							if (!r.exc) {
								nts.utils.play_sound("delete");
								nts.model.clear_doc(frm.doctype, frm.docname);
								window.history.back();
							}
						},
					});
				}
			);
		};

		frm.set_query("default_common_code", function (doc) {
			return {
				filters: {
					code_list: doc.name,
				},
			};
		});
	},
});
