// Copyright (c) 2023, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
nts.provide("prodman.bom");

nts.ui.form.on("BOM Creator", {
	setup(frm) {
		frm.trigger("set_queries");
	},

	setup_bom_creator(frm) {
		frm.dashboard.clear_comment();

		if (!frm.is_new()) {
			if (!nts.bom_configurator || nts.bom_configurator.bom_configurator !== frm.doc.name) {
				frm.trigger("build_tree");
			}
		} else if (!frm.doc.items?.length) {
			let $parent = $(frm.fields_dict["bom_creator"].wrapper);
			$parent.empty();
			frm.trigger("make_new_entry");
		}
	},

	build_tree(frm) {
		let $parent = $(frm.fields_dict["bom_creator"].wrapper);
		$parent.empty();
		frm.toggle_enable("item_code", false);

		nts.require("bom_configurator.bundle.js").then(() => {
			nts.bom_configurator = new nts.ui.BOMConfigurator({
				wrapper: $parent,
				page: $parent,
				frm: frm,
				bom_configurator: frm.doc.name,
			});
		});
	},

	make_new_entry(frm) {
		let dialog = new nts.ui.Dialog({
			title: __("Multi-level BOM Creator"),
			fields: [
				{
					label: __("Name"),
					fieldtype: "Data",
					fieldname: "name",
					reqd: 1,
				},
				{ fieldtype: "Column Break" },
				{
					label: __("Company"),
					fieldtype: "Link",
					fieldname: "company",
					options: "Company",
					reqd: 1,
					default: nts.defaults.get_user_default("Company"),
				},
				{ fieldtype: "Section Break" },
				{
					label: __("Item Code (Final Product)"),
					fieldtype: "Link",
					fieldname: "item_code",
					options: "Item",
					reqd: 1,
				},
				{ fieldtype: "Column Break" },
				{
					label: __("Quantity"),
					fieldtype: "Float",
					fieldname: "qty",
					reqd: 1,
					default: 1.0,
				},
				{ fieldtype: "Section Break" },
				{
					label: __("Currency"),
					fieldtype: "Link",
					fieldname: "currency",
					options: "Currency",
					reqd: 1,
					default: nts.defaults.get_global_default("currency"),
				},
				{ fieldtype: "Column Break" },
				{
					label: __("Conversion Rate"),
					fieldtype: "Float",
					fieldname: "conversion_rate",
					reqd: 1,
					default: 1.0,
				},
			],
			primary_action_label: __("Create"),
			primary_action: (values) => {
				values.doctype = frm.doc.doctype;
				nts.db.insert(values).then((doc) => {
					nts.set_route("Form", doc.doctype, doc.name);
				});
			},
		});

		dialog.fields_dict.item_code.get_query = "prodman.controllers.queries.item_query";
		dialog.show();
	},

	set_queries(frm) {
		frm.set_query("bom_no", "items", function (doc, cdt, cdn) {
			let item = nts.get_doc(cdt, cdn);
			return {
				filters: {
					item: item.item_code,
				},
			};
		});
		frm.set_query("item_code", "items", function () {
			return {
				query: "prodman.controllers.queries.item_query",
			};
		});
		frm.set_query("fg_item", "items", function () {
			return {
				query: "prodman.controllers.queries.item_query",
			};
		});
	},

	refresh(frm) {
		frm.trigger("setup_bom_creator");
		frm.trigger("set_root_item");
		frm.trigger("add_custom_buttons");
	},

	set_root_item(frm) {
		if (frm.is_new() && frm.doc.items?.length) {
			nts.model.set_value(frm.doc.items[0].doctype, frm.doc.items[0].name, "is_root", 1);
		}
	},

	add_custom_buttons(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Rebuild Tree"), () => {
				frm.trigger("build_tree");
			});
		}

		if (frm.doc.docstatus === 1 && frm.doc.status !== "Completed") {
			frm.add_custom_button(__("Create Multi-level BOM"), () => {
				frm.trigger("create_multi_level_bom");
			});
		}
	},

	create_multi_level_bom(frm) {
		frm.call({
			method: "enqueue_create_boms",
			doc: frm.doc,
		});
	},
});

nts.ui.form.on("BOM Creator Item", {
	item_code(frm, cdt, cdn) {
		let item = nts.get_doc(cdt, cdn);
		if (item.item_code && item.is_root) {
			nts.model.set_value(cdt, cdn, "fg_item", item.item_code);
		}
	},

	do_not_explode(frm, cdt, cdn) {
		let item = nts.get_doc(cdt, cdn);
		if (!item.do_not_explode) {
			frm.call({
				method: "get_default_bom",
				doc: frm.doc,
				args: {
					item_code: item.item_code,
				},
				callback(r) {
					if (r.message) {
						nts.model.set_value(cdt, cdn, "bom_no", r.message);
					}
				},
			});
		} else {
			nts.model.set_value(cdt, cdn, "bom_no", "");
		}
	},
});

prodman.bom.BomConfigurator = class BomConfigurator extends prodman.TransactionController {
	conversion_rate(doc) {
		if (this.frm.doc.currency === this.get_company_currency()) {
			this.frm.set_value("conversion_rate", 1.0);
		} else {
			prodman.bom.update_cost(doc);
		}
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
		}
	}
};

extend_cscript(cur_frm.cscript, new prodman.bom.BomConfigurator({ frm: cur_frm }));
