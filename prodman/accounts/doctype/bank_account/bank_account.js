// Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("Bank Account", {
	setup: function (frm) {
		frm.set_query("account", function () {
			return {
				filters: {
					account_type: "Bank",
					company: frm.doc.company,
					is_group: 0,
				},
			};
		});
		frm.set_query("party_type", function () {
			return {
				query: "prodman.setup.doctype.party_type.party_type.get_party_type",
			};
		});
	},
	refresh: function (frm) {
		nts .dynamic_link = { doc: frm.doc, fieldname: "name", doctype: "Bank Account" };

		frm.toggle_display(["address_html", "contact_html"], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			nts .contacts.clear_address_and_contact(frm);
		} else {
			nts .contacts.render_address_and_contact(frm);
		}

		if (frm.doc.integration_id) {
			frm.add_custom_button(__("Unlink external integrations"), function () {
				nts .confirm(
					__(
						"This action will unlink this account from any external service integrating prodman with your bank accounts. It cannot be undone. Are you certain ?"
					),
					function () {
						frm.set_value("integration_id", "");
					}
				);
			});
		}
	},

	is_company_account: function (frm) {
		frm.set_df_property("account", "reqd", frm.doc.is_company_account);
	},
});
