// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Customer", {
	setup: function (frm) {
		frm.make_methods = {
			Quotation: () =>
				nts.model.open_mapped_doc({
					method: "prodman.selling.doctype.customer.customer.make_quotation",
					frm: cur_frm,
				}),
			Opportunity: () =>
				nts.model.open_mapped_doc({
					method: "prodman.selling.doctype.customer.customer.make_opportunity",
					frm: cur_frm,
				}),
		};

		frm.add_fetch("lead_name", "company_name", "customer_name");
		frm.add_fetch("default_sales_partner", "commission_rate", "default_commission_rate");
		frm.set_query("default_price_list", { selling: 1 });
		frm.set_query("account", "accounts", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			let filters = {
				account_type: "Receivable",
				root_type: "Asset",
				company: d.company,
				is_group: 0,
			};

			if (doc.party_account_currency) {
				$.extend(filters, { account_currency: doc.party_account_currency });
			}
			return {
				filters: filters,
			};
		});

		frm.set_query("advance_account", "accounts", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					account_type: "Receivable",
					root_type: "Liability",
					company: d.company,
					is_group: 0,
				},
			};
		});

		if (frm.doc.__islocal == 1) {
			frm.set_value("represents_company", "");
		}

		frm.set_query("customer_primary_contact", function (doc) {
			return {
				query: "prodman.selling.doctype.customer.customer.get_customer_primary_contact",
				filters: {
					customer: doc.name,
				},
			};
		});
		frm.set_query("customer_primary_address", function (doc) {
			return {
				filters: {
					link_doctype: "Customer",
					link_name: doc.name,
				},
			};
		});

		frm.set_query("default_bank_account", function () {
			return {
				filters: {
					is_company_account: 1,
				},
			};
		});

		frm.set_query("user", "portal_users", function () {
			return {
				filters: {
					ignore_user_type: true,
				},
			};
		});
	},
	customer_primary_address: function (frm) {
		if (frm.doc.customer_primary_address) {
			nts.call({
				method: "nts.contacts.doctype.address.address.get_address_display",
				args: {
					address_dict: frm.doc.customer_primary_address,
				},
				callback: function (r) {
					frm.set_value("primary_address", r.message);
				},
			});
		}
		if (!frm.doc.customer_primary_address) {
			frm.set_value("primary_address", "");
		}
	},

	is_internal_customer: function (frm) {
		if (frm.doc.is_internal_customer == 1) {
			frm.toggle_reqd("represents_company", true);
		} else {
			frm.toggle_reqd("represents_company", false);
		}
	},

	customer_primary_contact: function (frm) {
		if (!frm.doc.customer_primary_contact) {
			frm.set_value("mobile_no", "");
			frm.set_value("email_id", "");
		}
	},

	loyalty_program: function (frm) {
		if (frm.doc.loyalty_program) {
			frm.set_value("loyalty_program_tier", null);
		}
	},

	refresh: function (frm) {
		if (nts.defaults.get_default("cust_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			prodman.toggle_naming_series();
		}

		if (!frm.doc.__islocal) {
			nts.contacts.render_address_and_contact(frm);

			// custom buttons

			frm.add_custom_button(
				__("Accounts Receivable"),
				function () {
					nts.set_route("query-report", "Accounts Receivable", {
						party_type: "Customer",
						party: frm.doc.name,
					});
				},
				__("View")
			);

			frm.add_custom_button(
				__("Accounting Ledger"),
				function () {
					nts.set_route("query-report", "General Ledger", {
						party_type: "Customer",
						party: frm.doc.name,
						party_name: frm.doc.customer_name,
					});
				},
				__("View")
			);

			frm.add_custom_button(
				__("Pricing Rule"),
				function () {
					prodman.utils.make_pricing_rule(frm.doc.doctype, frm.doc.name);
				},
				__("Create")
			);

			frm.add_custom_button(
				__("Get Customer Group Details"),
				function () {
					frm.trigger("get_customer_group_details");
				},
				__("Actions")
			);

			if (cint(nts.defaults.get_default("enable_common_party_accounting"))) {
				frm.add_custom_button(
					__("Link with Supplier"),
					function () {
						frm.trigger("show_party_link_dialog");
					},
					__("Actions")
				);
			}

			// indicator
			prodman.utils.set_party_dashboard_indicators(frm);
		} else {
			nts.contacts.clear_address_and_contact(frm);
		}

		var grid = cur_frm.get_field("sales_team").grid;
		grid.set_column_disp("allocated_amount", false);
		grid.set_column_disp("incentives", false);
	},
	validate: function (frm) {
		if (frm.doc.lead_name) nts.model.clear_doc("Lead", frm.doc.lead_name);
	},
	get_customer_group_details: function (frm) {
		nts.call({
			method: "get_customer_group_details",
			doc: frm.doc,
			callback: function () {
				frm.refresh();
			},
		});
	},
	show_party_link_dialog: function (frm) {
		const dialog = new nts.ui.Dialog({
			title: __("Select a Supplier"),
			fields: [
				{
					fieldtype: "Link",
					label: __("Supplier"),
					options: "Supplier",
					fieldname: "supplier",
					reqd: 1,
				},
			],
			primary_action: function ({ supplier }) {
				nts.call({
					method: "prodman.accounts.doctype.party_link.party_link.create_party_link",
					args: {
						primary_role: "Customer",
						primary_party: frm.doc.name,
						secondary_party: supplier,
					},
					freeze: true,
					callback: function () {
						dialog.hide();
						nts.msgprint({
							message: __("Successfully linked to Supplier"),
							alert: true,
						});
					},
					error: function () {
						dialog.hide();
						nts.msgprint({
							message: __("Linking to Supplier Failed. Please try again."),
							title: __("Linking Failed"),
							indicator: "red",
						});
					},
				});
			},
			primary_action_label: __("Create Link"),
		});
		dialog.show();
	},
});
