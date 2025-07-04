// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.provide("prodman.bom");

nts.ui.form.on("BOM", {
	setup(frm) {
		frm.custom_make_buttons = {
			"Work Order": "Work Order",
			"Quality Inspection": "Quality Inspection",
		};

		frm.set_query("bom_no", "items", function () {
			return {
				filters: {
					currency: frm.doc.currency,
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("source_warehouse", "items", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("item", function () {
			return {
				query: "prodman.manufacturing.doctype.bom.bom.item_query",
				filters: {
					is_stock_item: 1,
				},
			};
		});

		frm.set_query("project", function () {
			return {
				filters: [["Project", "status", "not in", "Completed, Cancelled"]],
			};
		});

		frm.set_query("item_code", "items", function (doc) {
			return {
				query: "prodman.manufacturing.doctype.bom.bom.item_query",
				filters: {
					include_item_in_manufacturing: 1,
					is_fixed_asset: 0,
				},
			};
		});

		frm.set_query("bom_no", "items", function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					item: d.item_code,
					is_active: 1,
					docstatus: 1,
				},
			};
		});
	},

	validate: function (frm) {
		if (frm.doc.fg_based_operating_cost && frm.doc.with_operations) {
			nts.throw({
				message: __("Please check either with operations or FG Based Operating Cost."),
				title: __("Mandatory"),
			});
		}
	},

	with_operations: function (frm) {
		frm.set_df_property("fg_based_operating_cost", "hidden", frm.doc.with_operations ? 1 : 0);
	},

	fg_based_operating_cost: function (frm) {
		frm.set_df_property("with_operations", "hidden", frm.doc.fg_based_operating_cost ? 1 : 0);
	},

	onload_post_render: function (frm) {
		frm.get_field("items").grid.set_multiple_add("item_code", "qty");
	},

	refresh(frm) {
		frm.toggle_enable("item", frm.doc.__islocal);

		frm.set_indicator_formatter("item_code", function (doc) {
			if (doc.original_item) {
				return doc.item_code != doc.original_item ? "orange" : "";
			}
			return "";
		});

		if (!frm.is_new() && frm.doc.docstatus < 2) {
			frm.add_custom_button(__("Update Cost"), function () {
				frm.events.update_cost(frm, true);
			});
			frm.add_custom_button(__("Browse BOM"), function () {
				nts.route_options = {
					bom: frm.doc.name,
				};
				nts.set_route("Tree", "BOM");
			});
		}

		if (!frm.is_new() && !frm.doc.docstatus == 0) {
			frm.add_custom_button(__("New Version"), function () {
				let new_bom = nts.model.copy_doc(frm.doc);
				nts.set_route("Form", "BOM", new_bom.name);
			});
		}

		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(
				__("Work Order"),
				function () {
					frm.trigger("make_work_order");
				},
				__("Create")
			);

			if (frm.doc.has_variants) {
				frm.add_custom_button(
					__("Variant BOM"),
					function () {
						frm.trigger("make_variant_bom");
					},
					__("Create")
				);
			}

			if (frm.doc.inspection_required) {
				frm.add_custom_button(
					__("Quality Inspection"),
					function () {
						frm.trigger("make_quality_inspection");
					},
					__("Create")
				);
			}

			frm.page.set_inner_btn_group_as_primary(__("Create"));
		}

		if (frm.doc.items && frm.doc.allow_alternative_item) {
			const has_alternative = frm.doc.items.find((i) => i.allow_alternative_item === 1);
			if (frm.doc.docstatus == 0 && has_alternative) {
				frm.add_custom_button(__("Alternate Item"), () => {
					prodman.utils.select_alternate_items({
						frm: frm,
						child_docname: "items",
						warehouse_field: "source_warehouse",
						child_doctype: "BOM Item",
						original_item_field: "original_item",
						condition: (d) => {
							if (d.allow_alternative_item) {
								return true;
							}
						},
					});
				});
			}
		}

		if (frm.doc.has_variants) {
			frm.set_intro(
				__("This is a Template BOM and will be used to make the work order for {0} of the item {1}", [
					`<a class="variants-intro">variants</a>`,
					`<a href="/app/item/${frm.doc.item}">${frm.doc.item}</a>`,
				]),
				true
			);

			frm.$wrapper.find(".variants-intro").on("click", () => {
				nts.set_route("List", "Item", { variant_of: frm.doc.item });
			});
		}
	},

	make_work_order(frm) {
		frm.events.setup_variant_prompt(
			frm,
			"Work Order",
			(frm, item, data, variant_items, use_multi_level_bom) => {
				nts.call({
					method: "prodman.manufacturing.doctype.work_order.work_order.make_work_order",
					args: {
						bom_no: frm.doc.name,
						item: item,
						qty: data.qty || 0.0,
						project: frm.doc.project,
						variant_items: variant_items,
						use_multi_level_bom: use_multi_level_bom,
					},
					freeze: true,
					callback(r) {
						if (r.message) {
							let doc = nts.model.sync(r.message)[0];
							nts.set_route("Form", doc.doctype, doc.name);
						}
					},
				});
			}
		);
	},

	make_variant_bom(frm) {
		frm.events.setup_variant_prompt(
			frm,
			"Variant BOM",
			(frm, item, data, variant_items) => {
				nts.call({
					method: "prodman.manufacturing.doctype.bom.bom.make_variant_bom",
					args: {
						source_name: frm.doc.name,
						bom_no: frm.doc.name,
						item: item,
						variant_items: variant_items,
					},
					freeze: true,
					callback(r) {
						if (r.message) {
							let doc = nts.model.sync(r.message)[0];
							nts.set_route("Form", doc.doctype, doc.name);
						}
					},
				});
			},
			true
		);
	},

	setup_variant_prompt(frm, title, callback, skip_qty_field) {
		const fields = [];

		if (frm.doc.has_variants) {
			fields.push({
				fieldtype: "Link",
				label: __("Variant Item"),
				fieldname: "item",
				options: "Item",
				reqd: 1,
				get_query() {
					return {
						query: "prodman.controllers.queries.item_query",
						filters: {
							variant_of: frm.doc.item,
						},
					};
				},
			});
		}

		if (!skip_qty_field) {
			fields.push({
				fieldtype: "Float",
				label: __("Qty To Manufacture"),
				fieldname: "qty",
				reqd: 1,
				default: 1,
				onchange: () => {
					const { quantity, items: rm } = frm.doc;
					const variant_items_map = rm.reduce((acc, item) => {
						acc[item.item_code] = item.qty;
						return acc;
					}, {});
					const mf_qty = cur_dialog.fields_list.filter((f) => f.df.fieldname === "qty")[0]?.value;
					const items = cur_dialog.fields.filter((f) => f.fieldname === "items")[0]?.data;

					if (!items) {
						return;
					}

					items.forEach((item) => {
						item.qty = (variant_items_map[item.item_code] * mf_qty) / quantity;
					});

					cur_dialog.refresh();
				},
			});

			fields.push({
				fieldtype: "Check",
				label: __("Use Multi-Level BOM"),
				fieldname: "use_multi_level_bom",
				default: frm.doc?.__onload.use_multi_level_bom,
			});
		}

		var has_template_rm = frm.doc.items.filter((d) => d.has_variants === 1) || [];
		if (has_template_rm && has_template_rm.length > 0) {
			fields.push({
				fieldname: "items",
				fieldtype: "Table",
				label: __("Raw Materials"),
				depends_on: "eval:!doc.use_multi_level_bom",
				fields: [
					{
						fieldname: "item_code",
						options: "Item",
						label: __("Template Item"),
						fieldtype: "Link",
						in_list_view: 1,
						reqd: 1,
						get_query() {
							return {
								filters: {
									has_variants: 1,
								},
							};
						},
					},
					{
						fieldname: "variant_item_code",
						options: "Item",
						label: __("Variant Item"),
						fieldtype: "Link",
						in_list_view: 1,
						reqd: 1,
						get_query(data) {
							if (!data.item_code) {
								nts.throw(__("Select template item"));
							}

							return {
								query: "prodman.controllers.queries.item_query",
								filters: {
									variant_of: data.item_code,
								},
							};
						},
						change() {
							let doc = this.doc;
							if (!doc.qty) {
								doc.qty = 1.0;
								this.grid.set_value("qty", 1.0, doc);
							}
						},
					},
					{
						fieldname: "qty",
						label: __("Quantity"),
						fieldtype: "Float",
						in_list_view: 1,
						reqd: 1,
					},
					{
						fieldname: "source_warehouse",
						label: __("Source Warehouse"),
						fieldtype: "Link",
						options: "Warehouse",
					},
					{
						fieldname: "operation",
						label: __("Operation"),
						fieldtype: "Data",
						hidden: 1,
					},
				],
				in_place_edit: true,
				data: [],
				get_data() {
					return [];
				},
			});
		}

		let dialog = nts.prompt(
			fields,
			(data) => {
				let item = data.item || frm.doc.item;
				let variant_items = data.items || [];
				let use_multi_level_bom = data.use_multi_level_bom || 0;

				variant_items.forEach((d) => {
					if (!d.variant_item_code && !use_multi_level_bom) {
						nts.throw(__("Select variant item code for the template item {0}", [d.item_code]));
					}
				});

				callback(frm, item, data, variant_items, use_multi_level_bom);
			},
			__(title),
			__("Create")
		);

		has_template_rm.forEach((d) => {
			dialog.fields_dict.items.df.data.push({
				item_code: d.item_code,
				variant_item_code: "",
				qty: (d.qty / frm.doc.quantity) * (dialog.fields_dict.qty.value || 1),
				source_warehouse: d.source_warehouse,
				operation: d.operation,
			});
		});

		if (has_template_rm && has_template_rm.length) {
			dialog.fields_dict.items.grid.refresh();
		}
	},

	make_quality_inspection(frm) {
		nts.model.open_mapped_doc({
			method: "prodman.stock.doctype.quality_inspection.quality_inspection.make_quality_inspection",
			frm: frm,
		});
	},

	update_cost(frm, save_doc = false) {
		return nts.call({
			doc: frm.doc,
			method: "update_cost",
			freeze: true,
			args: {
				update_parent: true,
				save: save_doc,
				from_child_bom: false,
			},
			callback(r) {
				refresh_field("items");
				if (!r.exc) frm.refresh_fields();
			},
		});
	},

	rm_cost_as_per(frm) {
		if (["Valuation Rate", "Last Purchase Rate"].includes(frm.doc.rm_cost_as_per)) {
			frm.set_value("plc_conversion_rate", 1.0);
		}
	},

	routing(frm) {
		if (frm.doc.routing) {
			nts.call({
				doc: frm.doc,
				method: "get_routing",
				freeze: true,
				callback(r) {
					if (!r.exc) {
						frm.refresh_fields();
						prodman.bom.calculate_op_cost(frm.doc);
						prodman.bom.calculate_total(frm.doc);
					}
				},
			});
		}
	},

	process_loss_percentage(frm) {
		let qty = 0.0;
		if (frm.doc.process_loss_percentage) {
			qty = (frm.doc.quantity * frm.doc.process_loss_percentage) / 100;
		}

		frm.set_value("process_loss_qty", qty);
	},
});

prodman.bom.BomController = class BomController extends prodman.TransactionController {
	conversion_rate(doc) {
		if (this.frm.doc.currency === this.get_company_currency()) {
			this.frm.set_value("conversion_rate", 1.0);
		} else {
			prodman.bom.update_cost(doc);
		}
	}

	item_code(doc, cdt, cdn) {
		var scrap_items = false;
		var child = locals[cdt][cdn];
		if (child.doctype == "BOM Scrap Item") {
			scrap_items = true;
		}

		if (child.bom_no) {
			child.bom_no = "";
		}

		if (doc.item == child.item_code) {
			child.do_not_explode = 1;
		}

		get_bom_material_detail(doc, cdt, cdn, scrap_items);
	}

	buying_price_list(doc) {
		this.apply_price_list();
	}

	plc_conversion_rate(doc) {
		if (!this.in_apply_price_list) {
			this.apply_price_list(null, true);
		}
	}

	conversion_factor(doc, cdt, cdn) {
		if (nts.meta.get_docfield(cdt, "stock_qty", cdn)) {
			var item = nts.get_doc(cdt, cdn);
			nts.model.round_floats_in(item, ["qty", "conversion_factor"]);
			item.stock_qty = flt(item.qty * item.conversion_factor, precision("stock_qty", item));
			refresh_field("stock_qty", item.name, item.parentfield);
			this.toggle_conversion_factor(item);
			this.frm.events.update_cost(this.frm);
		}
	}
};

extend_cscript(cur_frm.cscript, new prodman.bom.BomController({ frm: cur_frm }));

cur_frm.cscript.hour_rate = function (doc) {
	prodman.bom.calculate_op_cost(doc);
	prodman.bom.calculate_total(doc);
};

cur_frm.cscript.time_in_mins = cur_frm.cscript.hour_rate;

cur_frm.cscript.bom_no = function (doc, cdt, cdn) {
	get_bom_material_detail(doc, cdt, cdn, false);
};

cur_frm.cscript.is_default = function (doc) {
	if (doc.is_default) cur_frm.set_value("is_active", 1);
};

var get_bom_material_detail = function (doc, cdt, cdn, scrap_items) {
	if (!doc.company) {
		nts.throw({ message: __("Please select a Company first."), title: __("Mandatory") });
	}

	var d = locals[cdt][cdn];
	if (d.item_code) {
		return nts.call({
			doc: doc,
			method: "get_bom_material_detail",
			args: {
				company: doc.company,
				item_code: d.item_code,
				bom_no: d.bom_no != null ? d.bom_no : "",
				scrap_items: scrap_items,
				qty: d.qty,
				stock_qty: d.stock_qty,
				include_item_in_manufacturing: d.include_item_in_manufacturing,
				uom: d.uom,
				stock_uom: d.stock_uom,
				conversion_factor: d.conversion_factor,
				sourced_by_supplier: d.sourced_by_supplier,
				do_not_explode: d.do_not_explode,
			},
			callback: function (r) {
				d = locals[cdt][cdn];

				$.extend(d, r.message);
				refresh_field("items");
				refresh_field("scrap_items");

				doc = locals[doc.doctype][doc.name];
				prodman.bom.calculate_rm_cost(doc);
				prodman.bom.calculate_scrap_materials_cost(doc);
				prodman.bom.calculate_total(doc);
			},
			freeze: true,
		});
	}
};

cur_frm.cscript.qty = function (doc) {
	prodman.bom.calculate_rm_cost(doc);
	prodman.bom.calculate_scrap_materials_cost(doc);
	prodman.bom.calculate_total(doc);
};

cur_frm.cscript.rate = function (doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	const is_scrap_item = cdt == "BOM Scrap Item";

	if (d.bom_no) {
		nts.msgprint(__("You cannot change the rate if BOM is mentioned against any Item."));
		get_bom_material_detail(doc, cdt, cdn, is_scrap_item);
	} else {
		prodman.bom.calculate_rm_cost(doc);
		prodman.bom.calculate_scrap_materials_cost(doc);
		prodman.bom.calculate_total(doc);
	}
};

prodman.bom.update_cost = function (doc) {
	prodman.bom.calculate_op_cost(doc);
	prodman.bom.calculate_rm_cost(doc);
	prodman.bom.calculate_scrap_materials_cost(doc);
	prodman.bom.calculate_total(doc);
};

prodman.bom.calculate_op_cost = function (doc) {
	doc.operating_cost = 0.0;
	doc.base_operating_cost = 0.0;

	if (doc.with_operations) {
		doc.operations.forEach((item) => {
			let operating_cost = flt((flt(item.hour_rate) * flt(item.time_in_mins)) / 60, 2);
			let base_operating_cost = flt(operating_cost * doc.conversion_rate, 2);
			nts.model.set_value("BOM Operation", item.name, {
				operating_cost: operating_cost,
				base_operating_cost: base_operating_cost,
			});

			doc.operating_cost += operating_cost;
			doc.base_operating_cost += base_operating_cost;
		});
	} else if (doc.fg_based_operating_cost) {
		let total_operating_cost = doc.quantity * flt(doc.operating_cost_per_bom_quantity);
		doc.operating_cost = total_operating_cost;
		doc.base_operating_cost = flt(total_operating_cost * doc.conversion_rate, 2);
	}
	refresh_field(["operating_cost", "base_operating_cost"]);
};

// rm : raw material
prodman.bom.calculate_rm_cost = function (doc) {
	var rm = doc.items || [];
	var total_rm_cost = 0;
	var base_total_rm_cost = 0;
	for (var i = 0; i < rm.length; i++) {
		var amount = flt(rm[i].rate) * flt(rm[i].qty);
		var base_amount = amount * flt(doc.conversion_rate);

		nts.model.set_value(
			"BOM Item",
			rm[i].name,
			"base_rate",
			flt(rm[i].rate) * flt(doc.conversion_rate)
		);
		nts.model.set_value("BOM Item", rm[i].name, "amount", amount);
		nts.model.set_value("BOM Item", rm[i].name, "base_amount", base_amount);
		nts.model.set_value(
			"BOM Item",
			rm[i].name,
			"qty_consumed_per_unit",
			flt(rm[i].stock_qty) / flt(doc.quantity)
		);

		total_rm_cost += amount;
		base_total_rm_cost += base_amount;
	}
	cur_frm.set_value("raw_material_cost", total_rm_cost);
	cur_frm.set_value("base_raw_material_cost", base_total_rm_cost);
};

// sm : scrap material
prodman.bom.calculate_scrap_materials_cost = function (doc) {
	var sm = doc.scrap_items || [];
	var total_sm_cost = 0;
	var base_total_sm_cost = 0;

	for (var i = 0; i < sm.length; i++) {
		var base_rate = flt(sm[i].rate) * flt(doc.conversion_rate);
		var amount = flt(sm[i].rate) * flt(sm[i].stock_qty);
		var base_amount = amount * flt(doc.conversion_rate);

		nts.model.set_value("BOM Scrap Item", sm[i].name, "base_rate", base_rate);
		nts.model.set_value("BOM Scrap Item", sm[i].name, "amount", amount);
		nts.model.set_value("BOM Scrap Item", sm[i].name, "base_amount", base_amount);

		total_sm_cost += amount;
		base_total_sm_cost += base_amount;
	}

	cur_frm.set_value("scrap_material_cost", total_sm_cost);
	cur_frm.set_value("base_scrap_material_cost", base_total_sm_cost);
};

// Calculate Total Cost
prodman.bom.calculate_total = function (doc) {
	var total_cost = flt(doc.operating_cost) + flt(doc.raw_material_cost) - flt(doc.scrap_material_cost);
	var base_total_cost =
		flt(doc.base_operating_cost) + flt(doc.base_raw_material_cost) - flt(doc.base_scrap_material_cost);

	cur_frm.set_value("total_cost", total_cost);
	cur_frm.set_value("base_total_cost", base_total_cost);
};

cur_frm.cscript.validate = function (doc) {
	prodman.bom.update_cost(doc);
};

nts.ui.form.on("BOM Operation", "operation", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];

	if (!d.operation) return;

	nts.call({
		method: "nts.client.get",
		args: {
			doctype: "Operation",
			name: d.operation,
		},
		callback: function (data) {
			if (data.message.description) {
				nts.model.set_value(d.doctype, d.name, "description", data.message.description);
			}
			if (data.message.workstation) {
				nts.model.set_value(d.doctype, d.name, "workstation", data.message.workstation);
			}
		},
	});
});

nts.ui.form.on("BOM Operation", "workstation", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (!d.workstation) return;
	nts.call({
		method: "nts.client.get",
		args: {
			doctype: "Workstation",
			name: d.workstation,
		},
		callback: function (data) {
			nts.model.set_value(d.doctype, d.name, "base_hour_rate", data.message.hour_rate);
			nts.model.set_value(
				d.doctype,
				d.name,
				"hour_rate",
				flt(flt(data.message.hour_rate) / flt(frm.doc.conversion_rate)),
				2
			);

			prodman.bom.calculate_op_cost(frm.doc);
			prodman.bom.calculate_total(frm.doc);
		},
	});
});

nts.ui.form.on("BOM Item", {
	do_not_explode: function (frm, cdt, cdn) {
		get_bom_material_detail(frm.doc, cdt, cdn, false);
	},
});

nts.ui.form.on("BOM Item", "qty", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	d.stock_qty = d.qty * d.conversion_factor;
	refresh_field("stock_qty", d.name, d.parentfield);
});

nts.ui.form.on("BOM Item", "item_code", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	nts.db.get_value("Item", { name: d.item_code }, "allow_alternative_item", (r) => {
		d.allow_alternative_item = r.allow_alternative_item;
	});
	refresh_field("allow_alternative_item", d.name, d.parentfield);
});

nts.ui.form.on("BOM Item", "sourced_by_supplier", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.sourced_by_supplier) {
		d.rate = 0;
		refresh_field("rate", d.name, d.parentfield);
	}
});

nts.ui.form.on("BOM Item", "rate", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.sourced_by_supplier) {
		d.rate = 0;
		refresh_field("rate", d.name, d.parentfield);
	}
});

nts.ui.form.on("BOM Operation", "operations_remove", function (frm) {
	prodman.bom.calculate_op_cost(frm.doc);
	prodman.bom.calculate_total(frm.doc);
});

nts.ui.form.on("BOM Item", "items_remove", function (frm) {
	prodman.bom.calculate_rm_cost(frm.doc);
	prodman.bom.calculate_total(frm.doc);
});

nts.tour["BOM"] = [
	{
		fieldname: "item",
		title: "Item",
		description: __(
			"Select the Item to be manufactured. The Item name, UoM, Company, and Currency will be fetched automatically."
		),
	},
	{
		fieldname: "quantity",
		title: "Quantity",
		description: __(
			"Enter the quantity of the Item that will be manufactured from this Bill of Materials."
		),
	},
	{
		fieldname: "with_operations",
		title: "With Operations",
		description: __("To add Operations tick the 'With Operations' checkbox."),
	},
	{
		fieldname: "items",
		title: "Raw Materials",
		description: __("Select the raw materials (Items) required to manufacture the Item"),
	},
];

nts.ui.form.on("BOM Scrap Item", {
	item_code(frm, cdt, cdn) {
		const { item_code } = locals[cdt][cdn];
	},
});

function trigger_process_loss_qty_prompt(frm, cdt, cdn, item_code) {
	nts.prompt(
		{
			fieldname: "percent",
			fieldtype: "Percent",
			label: __("% Finished Item Quantity"),
			description:
				__("Set quantity of process loss item:") +
				` ${item_code} ` +
				__("as a percentage of finished item quantity"),
		},
		(data) => {
			const row = locals[cdt][cdn];
			row.stock_qty = (frm.doc.quantity * data.percent) / 100;
			row.qty = row.stock_qty / (row.conversion_factor || 1);
			refresh_field("scrap_items");
		},
		__("Set Process Loss Item Quantity"),
		__("Set Quantity")
	);
}
