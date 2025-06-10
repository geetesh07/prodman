// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Installation Note", {
	setup: function (frm) {
		nts.dynamic_link = { doc: frm.doc, fieldname: "customer", doctype: "Customer" };
		frm.set_query("customer_address", prodman.queries.address_query);
		frm.set_query("contact_person", prodman.queries.contact_query);
		frm.set_query("customer", prodman.queries.customer);
		frm.set_query("serial_and_batch_bundle", "items", (doc, cdt, cdn) => {
			let row = locals[cdt][cdn];
			return {
				filters: {
					item_code: row.item_code,
					voucher_type: doc.doctype,
					voucher_no: ["in", [doc.name, ""]],
					is_cancelled: 0,
				},
			};
		});
	},
	onload: function (frm) {
		if (!frm.doc.status) {
			frm.set_value({ status: "Draft" });
		}
		if (frm.doc.__islocal) {
			frm.set_value({ inst_date: nts.datetime.get_today() });
		}

		let sbb_field = frm.get_docfield("items", "serial_and_batch_bundle");
		if (sbb_field) {
			sbb_field.get_route_options_for_new_doc = (row) => {
				return {
					item_code: row.doc.item_code,
					voucher_type: frm.doc.doctype,
				};
			};
		}
	},
	customer: function (frm) {
		prodman.utils.get_party_details(frm);
	},
	customer_address: function (frm) {
		prodman.utils.get_address_display(frm);
	},
	contact_person: function (frm) {
		prodman.utils.get_contact_details(frm);
	},
});

nts.provide("prodman.selling");

// TODO commonify this code
prodman.selling.InstallationNote = class InstallationNote extends nts.ui.form.Controller {
	refresh() {
		var me = this;
		if (this.frm.doc.docstatus === 0) {
			this.frm.add_custom_button(
				__("From Delivery Note"),
				function () {
					prodman.utils.map_current_doc({
						method: "prodman.stock.doctype.delivery_note.delivery_note.make_installation_note",
						source_doctype: "Delivery Note",
						target: me.frm,
						date_field: "posting_date",
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							docstatus: 1,
							status: ["not in", ["Stopped", "Closed"]],
							per_installed: ["<", 99.99],
							company: me.frm.doc.company,
						},
					});
				},
				"fa fa-download",
				"btn-default"
			);
		}
	}
};

extend_cscript(cur_frm.cscript, new prodman.selling.InstallationNote({ frm: cur_frm }));
