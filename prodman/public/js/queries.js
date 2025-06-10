// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// searches for enabled users
nts.provide("prodman.queries");
$.extend(prodman.queries, {
	user: function () {
		return { query: "nts.core.doctype.user.user.user_query" };
	},

	lead: function () {
		return { query: "prodman.controllers.queries.lead_query" };
	},

	item: function (filters) {
		var args = { query: "prodman.controllers.queries.item_query" };
		if (filters) args["filters"] = filters;
		return args;
	},

	bom: function () {
		return { query: "prodman.controllers.queries.bom" };
	},

	task: function () {
		return { query: "prodman.projects.utils.query_task" };
	},

	customer_filter: function (doc) {
		if (!doc.customer) {
			cur_frm.scroll_to_field("customer");
			nts.show_alert({
				message: __("Please set {0} first.", [
					__(nts.meta.get_label(doc.doctype, "customer", doc.name)),
				]),
				indicator: "orange",
			});
		}

		return { filters: { customer: doc.customer } };
	},

	contact_query: function (doc) {
		if (nts.dynamic_link) {
			if (!doc[nts.dynamic_link.fieldname]) {
				cur_frm.scroll_to_field(nts.dynamic_link.fieldname);
				nts.show_alert({
					message: __("Please set {0} first.", [
						__(nts.meta.get_label(doc.doctype, nts.dynamic_link.fieldname, doc.name)),
					]),
					indicator: "orange",
				});
			}

			return {
				query: "nts.contacts.doctype.contact.contact.contact_query",
				filters: {
					link_doctype: nts.dynamic_link.doctype,
					link_name: doc[nts.dynamic_link.fieldname],
				},
			};
		}
	},

	company_contact_query: function (doc) {
		if (!doc.company) {
			nts.throw(__("Please set {0}", [__(nts.meta.get_label(doc.doctype, "company", doc.name))]));
		}

		return {
			query: "nts.contacts.doctype.contact.contact.contact_query",
			filters: { link_doctype: "Company", link_name: doc.company },
		};
	},

	address_query: function (doc) {
		if (nts.dynamic_link) {
			if (!doc[nts.dynamic_link.fieldname]) {
				cur_frm.scroll_to_field(nts.dynamic_link.fieldname);
				nts.show_alert({
					message: __("Please set {0} first.", [
						__(nts.meta.get_label(doc.doctype, nts.dynamic_link.fieldname, doc.name)),
					]),
					indicator: "orange",
				});
			}

			return {
				query: "nts.contacts.doctype.address.address.address_query",
				filters: {
					link_doctype: nts.dynamic_link.doctype,
					link_name: doc[nts.dynamic_link.fieldname],
				},
			};
		}
	},

	company_address_query: function (doc) {
		if (!doc.company) {
			cur_frm.scroll_to_field("company");
			nts.show_alert({
				message: __("Please set {0} first.", [
					__(nts.meta.get_label(doc.doctype, "company", doc.name)),
				]),
				indicator: "orange",
			});
		}

		return {
			query: "nts.contacts.doctype.address.address.address_query",
			filters: { link_doctype: "Company", link_name: doc.company },
		};
	},

	dispatch_address_query: function (doc) {
		var filters = { link_doctype: "Company", link_name: doc.company || "" };
		var is_drop_ship = doc.items.some((item) => item.delivered_by_supplier);
		if (is_drop_ship) filters = {};
		return {
			query: "nts.contacts.doctype.address.address.address_query",
			filters: filters,
		};
	},

	supplier_filter: function (doc) {
		if (!doc.supplier) {
			cur_frm.scroll_to_field("supplier");
			nts.show_alert({
				message: __("Please set {0} first.", [
					__(nts.meta.get_label(doc.doctype, "supplier", doc.name)),
				]),
				indicator: "orange",
			});
		}

		return { filters: { supplier: doc.supplier } };
	},

	lead_filter: function (doc) {
		if (!doc.lead) {
			cur_frm.scroll_to_field("lead");
			nts.show_alert({
				message: __("Please specify a {0} first.", [
					__(nts.meta.get_label(doc.doctype, "lead", doc.name)),
				]),
				indicator: "orange",
			});
		}

		return { filters: { lead: doc.lead } };
	},

	not_a_group_filter: function () {
		return { filters: { is_group: 0 } };
	},

	employee: function () {
		return { query: "prodman.controllers.queries.employee_query" };
	},

	warehouse: function (doc) {
		return {
			filters: [
				["Warehouse", "company", "in", ["", cstr(doc.company)]],
				["Warehouse", "is_group", "=", 0],
			],
		};
	},

	get_filtered_dimensions: function (doc, child_fields, dimension, company) {
		let account = "";

		child_fields.forEach((field) => {
			if (!account) {
				account = doc[field];
			}
		});

		return {
			query: "prodman.controllers.queries.get_filtered_dimensions",
			filters: {
				dimension: dimension,
				account: account,
				company: company,
			},
		};
	},
});

prodman.queries.setup_queries = function (frm, options, query_fn) {
	var me = this;
	var set_query = function (doctype, parentfield) {
		var link_fields = nts.meta.get_docfields(doctype, frm.doc.name, {
			fieldtype: "Link",
			options: options,
		});
		$.each(link_fields, function (i, df) {
			if (parentfield) {
				frm.set_query(df.fieldname, parentfield, query_fn);
			} else {
				frm.set_query(df.fieldname, query_fn);
			}
		});
	};

	set_query(frm.doc.doctype);

	// warehouse field in tables
	$.each(
		nts.meta.get_docfields(frm.doc.doctype, frm.doc.name, { fieldtype: "Table" }),
		function (i, df) {
			set_query(df.options, df.fieldname);
		}
	);
};

/* 	if item code is selected in child table
	then list down warehouses with its quantity
	else apply default filters.
*/
prodman.queries.setup_warehouse_query = function (frm) {
	frm.set_query("warehouse", "items", function (doc, cdt, cdn) {
		var row = locals[cdt][cdn];
		var filters = prodman.queries.warehouse(frm.doc);
		if (row.item_code) {
			$.extend(filters, { query: "prodman.controllers.queries.warehouse_query" });
			filters["filters"].push(["Bin", "item_code", "=", row.item_code]);
		}
		return filters;
	});
};
