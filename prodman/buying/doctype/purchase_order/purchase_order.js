// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.provide("prodman.buying");
nts.provide("prodman.accounts.dimensions");

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";

prodman.accounts.taxes.setup_tax_filters("Purchase Taxes and Charges");
prodman.accounts.taxes.setup_tax_validations("Purchase Order");
prodman.buying.setup_buying_controller();

nts.ui.form.on("Purchase Order", {
	setup: function (frm) {
		frm.ignore_doctypes_on_cancel_all = ["Unreconcile Payment", "Unreconcile Payment Entries"];
		if (frm.doc.is_old_subcontracting_flow) {
			frm.set_query("reserve_warehouse", "supplied_items", function () {
				return {
					filters: {
						company: frm.doc.company,
						name: ["!=", frm.doc.supplier_warehouse],
						is_group: 0,
					},
				};
			});
		}

		frm.set_indicator_formatter("item_code", function (doc) {
			let color;
			if (!doc.qty && frm.doc.has_unit_price_items) {
				color = "yellow";
			} else if (doc.qty <= doc.received_qty) {
				color = "green";
			} else {
				color = "orange";
			}
			return color;
		});

		frm.set_query("expense_account", "items", function () {
			return {
				query: "prodman.controllers.queries.get_expense_account",
				filters: { company: frm.doc.company },
			};
		});

		frm.set_query("fg_item", "items", function () {
			return {
				filters: {
					is_stock_item: 1,
					is_sub_contracted_item: 1,
					default_bom: ["!=", ""],
				},
			};
		});
	},

	company: function (frm) {
		prodman.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	refresh: function (frm) {
		if (frm.doc.is_old_subcontracting_flow) {
			frm.trigger("get_materials_from_supplier");

			$("a.grey-link").each(function () {
				var id = $(this).children(":first-child").attr("data-label");
				if (id == "Duplicate") {
					$(this).remove();
					return false;
				}
			});
		}

		if (frm.doc.docstatus == 0) {
			prodman.set_unit_price_items_note(frm);
		}
	},

	supplier: function (frm) {
		// Do not update if inter company reference is there as the details will already be updated
		if (frm.updating_party_details || frm.doc.inter_company_invoice_reference) return;

		if (frm.doc.__onload && frm.doc.__onload.load_after_mapping) return;

		prodman.utils.get_party_details(
			frm,
			"prodman.accounts.party.get_party_details",
			{
				posting_date: frm.doc.transaction_date,
				bill_date: frm.doc.bill_date,
				party: frm.doc.supplier,
				party_type: "Supplier",
				account: frm.doc.credit_to,
				price_list: frm.doc.buying_price_list,
				fetch_payment_terms_template: cint(!frm.doc.ignore_default_payment_terms_template),
			},
			function () {
				frm.set_df_property("apply_tds", "read_only", frm.supplier_tds ? 0 : 1);
				frm.set_df_property("tax_withholding_category", "hidden", frm.supplier_tds ? 0 : 1);
			}
		);
	},

	get_materials_from_supplier: function (frm) {
		let po_details = [];

		if (frm.doc.supplied_items && (flt(frm.doc.per_received) == 100 || frm.doc.status === "Closed")) {
			frm.doc.supplied_items.forEach((d) => {
				if (d.total_supplied_qty && d.total_supplied_qty != d.consumed_qty) {
					po_details.push(d.name);
				}
			});
		}

		if (po_details && po_details.length) {
			frm.add_custom_button(
				__("Return of Components"),
				() => {
					frm.call({
						method: "prodman.controllers.subcontracting_controller.get_materials_from_supplier",
						freeze: true,
						freeze_message: __("Creating Stock Entry"),
						args: {
							subcontract_order: frm.doc.name,
							rm_details: po_details,
							order_doctype: cur_frm.doc.doctype,
						},
						callback: function (r) {
							if (r && r.message) {
								const doc = nts.model.sync(r.message);
								nts.set_route("Form", doc[0].doctype, doc[0].name);
							}
						},
					});
				},
				__("Create")
			);
		}
	},

	onload: function (frm) {
		set_schedule_date(frm);
		if (!frm.doc.transaction_date) {
			frm.set_value("transaction_date", nts.datetime.get_today());
		}

		if (frm.doc.__onload && frm.doc.supplier) {
			if (frm.is_new()) {
				frm.doc.apply_tds = frm.doc.__onload.supplier_tds ? 1 : 0;
			}
			if (!frm.doc.__onload.supplier_tds) {
				frm.set_df_property("apply_tds", "read_only", 1);
			}
		}

		prodman.queries.setup_queries(frm, "Warehouse", function () {
			return prodman.queries.warehouse(frm.doc);
		});

		// On cancel and amending a purchase order with advance payment, reset advance paid amount
		if (frm.is_new()) {
			frm.set_value("advance_paid", 0);
		}
	},

	apply_tds: function (frm) {
		if (!frm.doc.apply_tds) {
			frm.set_value("tax_withholding_category", "");
		} else {
			frm.set_value("tax_withholding_category", frm.supplier_tds);
		}
	},

	get_subcontracting_boms_for_finished_goods: function (fg_item) {
		return nts.call({
			method: "prodman.subcontracting.doctype.subcontracting_bom.subcontracting_bom.get_subcontracting_boms_for_finished_goods",
			args: {
				fg_items: fg_item,
			},
		});
	},

	get_subcontracting_boms_for_service_item: function (service_item) {
		return nts.call({
			method: "prodman.subcontracting.doctype.subcontracting_bom.subcontracting_bom.get_subcontracting_boms_for_service_item",
			args: {
				service_item: service_item,
			},
		});
	},
});

nts.ui.form.on("Purchase Order Item", {
	schedule_date: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.schedule_date) {
			if (!frm.doc.schedule_date) {
				prodman.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "schedule_date");
			} else {
				set_schedule_date(frm);
			}
		}
	},

	item_code: async function (frm, cdt, cdn) {
		if (frm.doc.is_subcontracted && !frm.doc.is_old_subcontracting_flow) {
			var row = locals[cdt][cdn];

			if (row.item_code && !row.fg_item) {
				var result = await frm.events.get_subcontracting_boms_for_service_item(row.item_code);

				if (result.message && Object.keys(result.message).length) {
					var finished_goods = Object.keys(result.message);

					// Set FG if only one active Subcontracting BOM is found
					if (finished_goods.length === 1) {
						row.fg_item = result.message[finished_goods[0]].finished_good;
						row.uom = result.message[finished_goods[0]].finished_good_uom;
						refresh_field("items");
					} else {
						const dialog = new nts.ui.Dialog({
							title: __("Select Finished Good"),
							size: "small",
							fields: [
								{
									fieldname: "finished_good",
									fieldtype: "Autocomplete",
									label: __("Finished Good"),
									options: finished_goods,
								},
							],
							primary_action_label: __("Select"),
							primary_action: () => {
								var subcontracting_bom = result.message[dialog.get_value("finished_good")];

								if (subcontracting_bom) {
									row.fg_item = subcontracting_bom.finished_good;
									row.uom = subcontracting_bom.finished_good_uom;
									refresh_field("items");
								}

								dialog.hide();
							},
						});

						dialog.show();
					}
				}
			}
		}
	},

	fg_item: async function (frm, cdt, cdn) {
		if (frm.doc.is_subcontracted && !frm.doc.is_old_subcontracting_flow) {
			var row = locals[cdt][cdn];

			if (row.fg_item) {
				var result = await frm.events.get_subcontracting_boms_for_finished_goods(row.fg_item);

				if (result.message && Object.keys(result.message).length) {
					nts.model.set_value(cdt, cdn, "item_code", result.message.service_item);
					nts.model.set_value(
						cdt,
						cdn,
						"qty",
						flt(row.fg_item_qty) * flt(result.message.conversion_factor)
					);
					nts.model.set_value(cdt, cdn, "uom", result.message.service_item_uom);
				}
			}
		}
	},

	qty: async function (frm, cdt, cdn) {
		if (frm.doc.is_subcontracted && !frm.doc.is_old_subcontracting_flow) {
			var row = locals[cdt][cdn];

			if (row.fg_item) {
				var result = await frm.events.get_subcontracting_boms_for_finished_goods(row.fg_item);

				if (
					result.message &&
					row.item_code == result.message.service_item &&
					row.uom == result.message.service_item_uom
				) {
					nts.model.set_value(
						cdt,
						cdn,
						"fg_item_qty",
						flt(row.qty) / flt(result.message.conversion_factor)
					);
				}
			}
		}
	},
});

prodman.buying.PurchaseOrderController = class PurchaseOrderController extends (
	prodman.buying.BuyingController
) {
	setup() {
		this.frm.custom_make_buttons = {
			"Purchase Receipt": "Purchase Receipt",
			"Purchase Invoice": "Purchase Invoice",
			"Payment Entry": "Payment",
			"Subcontracting Order": "Subcontracting Order",
			"Stock Entry": "Material to Supplier",
		};

		super.setup();
	}

	refresh(doc, cdt, cdn) {
		var me = this;
		super.refresh();
		var allow_receipt = false;
		var is_drop_ship = false;

		for (var i in cur_frm.doc.items) {
			var item = cur_frm.doc.items[i];
			if (item.delivered_by_supplier !== 1) {
				allow_receipt = true;
			} else {
				is_drop_ship = true;
			}

			if (is_drop_ship && allow_receipt) {
				break;
			}
		}

		this.frm.set_df_property("drop_ship", "hidden", !is_drop_ship);

		if (doc.docstatus == 1) {
			this.frm.fields_dict.items_section.wrapper.addClass("hide-border");
			if (!this.frm.doc.set_warehouse) {
				this.frm.fields_dict.items_section.wrapper.removeClass("hide-border");
			}

			if (!["Closed", "Delivered"].includes(doc.status)) {
				if (
					this.frm.doc.status !== "Closed" &&
					flt(this.frm.doc.per_received) < 100 &&
					flt(this.frm.doc.per_billed) < 100
				) {
					if (!this.frm.doc.__onload || this.frm.doc.__onload.can_update_items) {
						this.frm.add_custom_button(__("Update Items"), () => {
							prodman.utils.update_child_items({
								frm: this.frm,
								child_docname: "items",
								child_doctype: "Purchase Order Detail",
								cannot_add_row: false,
							});
						});
					}
				}
				if (this.frm.has_perm("submit")) {
					if (flt(doc.per_billed) < 100 || flt(doc.per_received) < 100) {
						if (doc.status != "On Hold") {
							this.frm.add_custom_button(
								__("Hold"),
								() => this.hold_purchase_order(),
								__("Status")
							);
						} else {
							this.frm.add_custom_button(
								__("Resume"),
								() => this.unhold_purchase_order(),
								__("Status")
							);
						}
						this.frm.add_custom_button(
							__("Close"),
							() => this.close_purchase_order(),
							__("Status")
						);
					}
				}

				if (is_drop_ship && doc.status != "Delivered") {
					this.frm.add_custom_button(
						__("Delivered"),
						this.delivered_by_supplier.bind(this),
						__("Status")
					);

					this.frm.page.set_inner_btn_group_as_primary(__("Status"));
				}
			} else if (["Closed", "Delivered"].includes(doc.status)) {
				if (this.frm.has_perm("submit")) {
					this.frm.add_custom_button(
						__("Re-open"),
						() => this.unclose_purchase_order(),
						__("Status")
					);
				}
			}
			if (doc.status != "Closed") {
				if (doc.status != "On Hold") {
					if (flt(doc.per_received) < 100 && allow_receipt) {
						this.frm.add_custom_button(
							__("Purchase Receipt"),
							this.make_purchase_receipt,
							__("Create")
						);
						if (doc.is_subcontracted) {
							if (doc.is_old_subcontracting_flow) {
								if (me.has_unsupplied_items()) {
									cur_frm.add_custom_button(
										__("Material to Supplier"),
										function () {
											me.make_stock_entry();
										},
										__("Transfer")
									);
								}
							} else {
								if (!doc.items.every((item) => item.qty == item.subcontracted_quantity)) {
									this.frm.add_custom_button(
										__("Subcontracting Order"),
										() => {
											me.make_subcontracting_order();
										},
										__("Create")
									);
								}
							}
						}
					}
					// Please do not add precision in the below flt function
					if (flt(doc.per_billed) < 100)
						this.frm.add_custom_button(
							__("Purchase Invoice"),
							this.make_purchase_invoice,
							__("Create")
						);

					if (flt(doc.per_billed) < 100 && doc.status != "Delivered") {
						this.frm.add_custom_button(
							__("Payment"),
							() => this.make_payment_entry(),
							__("Create")
						);
					}

					if (flt(doc.per_billed) < 100) {
						this.frm.add_custom_button(
							__("Payment Request"),
							function () {
								me.make_payment_request();
							},
							__("Create")
						);
					}

					if (doc.docstatus === 1 && !doc.inter_company_order_reference) {
						let me = this;
						let internal = me.frm.doc.is_internal_supplier;
						if (internal) {
							let button_label =
								me.frm.doc.company === me.frm.doc.represents_company
									? "Internal Sales Order"
									: "Inter Company Sales Order";

							me.frm.add_custom_button(
								button_label,
								function () {
									me.make_inter_company_order(me.frm);
								},
								__("Create")
							);
						}
					}
				}

				cur_frm.page.set_inner_btn_group_as_primary(__("Create"));
			}
		} else if (doc.docstatus === 0) {
			cur_frm.cscript.add_from_mappers();
		}
	}

	get_items_from_open_material_requests() {
		prodman.utils.map_current_doc({
			method: "prodman.stock.doctype.material_request.material_request.make_purchase_order_based_on_supplier",
			args: {
				supplier: this.frm.doc.supplier,
			},
			source_doctype: "Material Request",
			source_name: this.frm.doc.supplier,
			target: this.frm,
			setters: {
				company: this.frm.doc.company,
			},
			get_query_filters: {
				docstatus: ["!=", 2],
				supplier: this.frm.doc.supplier,
			},
			get_query_method:
				"prodman.stock.doctype.material_request.material_request.get_material_requests_based_on_supplier",
		});
	}

	validate() {
		set_schedule_date(this.frm);
	}

	has_unsupplied_items() {
		return this.frm.doc["supplied_items"].some((item) => item.required_qty > item.supplied_qty);
	}

	make_stock_entry() {
		nts.call({
			method: "prodman.controllers.subcontracting_controller.make_rm_stock_entry",
			args: {
				subcontract_order: cur_frm.doc.name,
				order_doctype: cur_frm.doc.doctype,
			},
			callback: function (r) {
				var doclist = nts.model.sync(r.message);
				nts.set_route("Form", doclist[0].doctype, doclist[0].name);
			},
		});
	}

	make_inter_company_order(frm) {
		nts.model.open_mapped_doc({
			method: "prodman.buying.doctype.purchase_order.purchase_order.make_inter_company_sales_order",
			frm: frm,
		});
	}

	make_purchase_receipt() {
		nts.model.open_mapped_doc({
			method: "prodman.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
			frm: cur_frm,
			freeze_message: __("Creating Purchase Receipt ..."),
		});
	}

	make_purchase_invoice() {
		nts.model.open_mapped_doc({
			method: "prodman.buying.doctype.purchase_order.purchase_order.make_purchase_invoice",
			frm: cur_frm,
		});
	}

	make_subcontracting_order() {
		nts.model.open_mapped_doc({
			method: "prodman.buying.doctype.purchase_order.purchase_order.make_subcontracting_order",
			frm: cur_frm,
			freeze_message: __("Creating Subcontracting Order ..."),
		});
	}

	add_from_mappers() {
		var me = this;
		this.frm.add_custom_button(
			__("Material Request"),
			function () {
				prodman.utils.map_current_doc({
					method: "prodman.stock.doctype.material_request.material_request.make_purchase_order",
					source_doctype: "Material Request",
					target: me.frm,
					setters: {
						schedule_date: undefined,
					},
					get_query_filters: {
						material_request_type: "Purchase",
						docstatus: 1,
						status: ["!=", "Stopped"],
						per_ordered: ["<", 100],
						company: me.frm.doc.company,
					},
					allow_child_item_selection: true,
					child_fieldname: "items",
					child_columns: ["item_code", "qty", "ordered_qty"],
				});
			},
			__("Get Items From")
		);

		this.frm.add_custom_button(
			__("Supplier Quotation"),
			function () {
				prodman.utils.map_current_doc({
					method: "prodman.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
					source_doctype: "Supplier Quotation",
					target: me.frm,
					setters: {
						supplier: me.frm.doc.supplier,
						valid_till: undefined,
					},
					get_query_filters: {
						docstatus: 1,
						status: ["not in", ["Stopped", "Expired"]],
					},
				});
			},
			__("Get Items From")
		);

		this.frm.add_custom_button(
			__("Update Rate as per Last Purchase"),
			function () {
				nts.call({
					method: "get_last_purchase_rate",
					doc: me.frm.doc,
					callback: function (r, rt) {
						me.frm.dirty();
						me.frm.cscript.calculate_taxes_and_totals();
					},
				});
			},
			__("Tools")
		);

		this.frm.add_custom_button(
			__("Link to Material Request"),
			function () {
				var my_items = [];
				for (var i in me.frm.doc.items) {
					if (!me.frm.doc.items[i].material_request) {
						my_items.push(me.frm.doc.items[i].item_code);
					}
				}
				nts.call({
					method: "prodman.buying.utils.get_linked_material_requests",
					args: {
						items: my_items,
					},
					callback: function (r) {
						if (r.exc) return;

						var i = 0;
						var item_length = me.frm.doc.items.length;
						while (i < item_length) {
							var qty = me.frm.doc.items[i].qty;
							(r.message[0] || []).forEach(function (d) {
								if (
									d.qty > 0 &&
									qty > 0 &&
									me.frm.doc.items[i].item_code == d.item_code &&
									!me.frm.doc.items[i].material_request_item
								) {
									me.frm.doc.items[i].material_request = d.mr_name;
									me.frm.doc.items[i].material_request_item = d.mr_item;
									var my_qty = Math.min(qty, d.qty);
									qty = qty - my_qty;
									d.qty = d.qty - my_qty;
									me.frm.doc.items[i].stock_qty =
										my_qty * me.frm.doc.items[i].conversion_factor;
									me.frm.doc.items[i].qty = my_qty;

									nts.msgprint(
										"Assigning " +
											d.mr_name +
											" to " +
											d.item_code +
											" (row " +
											me.frm.doc.items[i].idx +
											")"
									);
									if (qty > 0) {
										nts.msgprint("Splitting " + qty + " units of " + d.item_code);
										var new_row = nts.model.add_child(
											me.frm.doc,
											me.frm.doc.items[i].doctype,
											"items"
										);
										item_length++;

										for (var key in me.frm.doc.items[i]) {
											new_row[key] = me.frm.doc.items[i][key];
										}

										new_row.idx = item_length;
										new_row["stock_qty"] = new_row.conversion_factor * qty;
										new_row["qty"] = qty;
										new_row["material_request"] = "";
										new_row["material_request_item"] = "";
									}
								}
							});
							i++;
						}
						refresh_field("items");
					},
				});
			},
			__("Tools")
		);
	}

	tc_name() {
		this.get_terms();
	}

	items_add(doc, cdt, cdn) {
		var row = nts.get_doc(cdt, cdn);
		if (doc.schedule_date) {
			row.schedule_date = doc.schedule_date;
			refresh_field("schedule_date", cdn, "items");
		} else {
			this.frm.script_manager.copy_from_first_row("items", row, ["schedule_date"]);
		}
	}

	unhold_purchase_order() {
		cur_frm.cscript.update_status("Resume", "Draft");
	}

	hold_purchase_order() {
		var me = this;
		var d = new nts.ui.Dialog({
			title: __("Reason for Hold"),
			fields: [
				{
					fieldname: "reason_for_hold",
					fieldtype: "Text",
					reqd: 1,
				},
			],
			primary_action: function () {
				var data = d.get_values();
				let reason_for_hold = "Reason for hold: " + data.reason_for_hold;

				nts.call({
					method: "nts.desk.form.utils.add_comment",
					args: {
						reference_doctype: me.frm.doctype,
						reference_name: me.frm.docname,
						content: __(reason_for_hold),
						comment_email: nts.session.user,
						comment_by: nts.session.user_fullname,
					},
					callback: function (r) {
						if (!r.exc) {
							me.update_status("Hold", "On Hold");
							d.hide();
						}
					},
				});
			},
		});
		d.show();
	}

	unclose_purchase_order() {
		cur_frm.cscript.update_status("Re-open", "Submitted");
	}

	close_purchase_order() {
		cur_frm.cscript.update_status("Close", "Closed");
	}

	delivered_by_supplier() {
		cur_frm.cscript.update_status("Deliver", "Delivered");
	}

	items_on_form_rendered() {
		set_schedule_date(this.frm);
	}

	schedule_date() {
		set_schedule_date(this.frm);
	}
};

// for backward compatibility: combine new and previous states
extend_cscript(cur_frm.cscript, new prodman.buying.PurchaseOrderController({ frm: cur_frm }));

cur_frm.cscript.update_status = function (label, status) {
	nts.call({
		method: "prodman.buying.doctype.purchase_order.purchase_order.update_status",
		args: { status: status, name: cur_frm.doc.name },
		callback: function (r) {
			cur_frm.set_value("status", status);
			cur_frm.reload_doc();
		},
	});
};

cur_frm.fields_dict["items"].grid.get_field("project").get_query = function (doc, cdt, cdn) {
	return {
		filters: [["Project", "status", "not in", "Completed, Cancelled"]],
	};
};

if (cur_frm.doc.is_old_subcontracting_flow) {
	cur_frm.fields_dict["items"].grid.get_field("bom").get_query = function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		return {
			filters: [
				["BOM", "item", "=", d.item_code],
				["BOM", "is_active", "=", "1"],
				["BOM", "docstatus", "=", "1"],
				["BOM", "company", "=", doc.company],
			],
		};
	};
}

function set_schedule_date(frm) {
	if (frm.doc.schedule_date) {
		prodman.utils.copy_value_in_all_rows(
			frm.doc,
			frm.doc.doctype,
			frm.doc.name,
			"items",
			"schedule_date"
		);
	}
}

nts.provide("prodman.buying");

nts.ui.form.on("Purchase Order", "is_subcontracted", function (frm) {
	if (frm.doc.is_old_subcontracting_flow) {
		prodman.buying.get_default_bom(frm);
	}
});
