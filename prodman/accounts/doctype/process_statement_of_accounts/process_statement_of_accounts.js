// Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("Process Statement Of Accounts", {
	view_properties: function (frm) {
		nts .route_options = { doc_type: "Customer" };
		nts .set_route("Form", "Customize Form");
	},
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Send Emails"), function () {
				if (frm.is_dirty()) nts .throw(__("Please save before proceeding."));
				nts .call({
					method: "prodman.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.send_emails",
					args: {
						document_name: frm.doc.name,
					},
					callback: function (r) {
						if (r && r.message) {
							nts .show_alert({ message: __("Emails Queued"), indicator: "blue" });
						} else {
							nts .msgprint(__("No Records for these settings."));
						}
					},
				});
			});
			frm.add_custom_button(__("Download"), function () {
				if (frm.is_dirty()) nts .throw(__("Please save before proceeding."));
				let url = nts .urllib.get_full_url(
					"/api/method/prodman.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.download_statements?" +
						"document_name=" +
						encodeURIComponent(frm.doc.name)
				);
				$.ajax({
					url: url,
					type: "GET",
					success: function (result) {
						if (jQuery.isEmptyObject(result)) {
							nts .msgprint(__("No Records for these settings."));
						} else {
							window.location = url;
						}
					},
				});
			});
		}
	},
	onload: function (frm) {
		frm.set_query("currency", function () {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
		frm.set_query("account", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("cost_center", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("project", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		if (frm.doc.__islocal) {
			frm.set_value("from_date", nts .datetime.add_months(nts .datetime.get_today(), -1));
			frm.set_value("to_date", nts .datetime.get_today());
		}
	},
	report: function (frm) {
		let filters = {
			company: frm.doc.company,
		};
		if (frm.doc.report == "Accounts Receivable") {
			filters["account_type"] = "Receivable";
		}
		frm.set_query("account", function () {
			return {
				filters: filters,
			};
		});
	},
	customer_collection: function (frm) {
		frm.set_value("collection_name", "");
		if (frm.doc.customer_collection) {
			frm.get_field("collection_name").set_label(frm.doc.customer_collection);
		}
	},
	frequency: function (frm) {
		if (frm.doc.frequency != "") {
			frm.set_value("start_date", nts .datetime.get_today());
		} else {
			frm.set_value("start_date", "");
		}
	},
	fetch_customers: function (frm) {
		if (frm.doc.collection_name) {
			nts .call({
				method: "prodman.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.fetch_customers",
				args: {
					customer_collection: frm.doc.customer_collection,
					collection_name: frm.doc.collection_name,
					primary_mandatory: frm.doc.primary_mandatory,
				},
				callback: function (r) {
					if (!r.exc) {
						if (r.message.length) {
							frm.clear_table("customers");
							for (const customer of r.message) {
								var row = frm.add_child("customers");
								row.customer = customer.name;
								row.primary_email = customer.primary_email;
								row.billing_email = customer.billing_email;
							}
							frm.refresh_field("customers");
						} else {
							nts .throw(__("No Customers found with selected options."));
						}
					}
				},
			});
		} else {
			nts .throw("Enter " + frm.doc.customer_collection + " name.");
		}
	},
});

nts .ui.form.on("Process Statement Of Accounts Customer", {
	customer: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (!row.customer) {
			return;
		}
		nts .call({
			method: "prodman.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.get_customer_emails",
			args: {
				customer_name: row.customer,
				primary_mandatory: frm.doc.primary_mandatory,
			},
			callback: function (r) {
				if (!r.exe) {
					if (r.message.length) {
						nts .model.set_value(cdt, cdn, "primary_email", r.message[0]);
						nts .model.set_value(cdt, cdn, "billing_email", r.message[1]);
					} else {
						return;
					}
				}
			},
		});
	},
});
