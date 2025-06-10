// Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("Accounting Dimension Filter", {
	refresh: function (frm, cdt, cdn) {
		let help_content = `<table class="table table-bordered" style="background-color: var(--scrollbar-track-color);">
				<tr><td>
					<p>
						<i class="fa fa-hand-right"></i>
						{{__('Note: On checking Is Mandatory the accounting dimension will become mandatory against that specific account for all accounting transactions')}}
					</p>
				</td></tr>
			</table>`;

		frm.set_df_property("dimension_filter_help", "options", help_content);
	},
	onload: function (frm) {
		frm.set_query("applicable_on_account", "accounts", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		nts .db.get_list("Accounting Dimension", { fields: ["document_type"] }).then((res) => {
			let options = ["Cost Center", "Project"];

			res.forEach((dimension) => {
				options.push(dimension.document_type);
			});

			frm.set_df_property("accounting_dimension", "options", options);
		});

		frm.trigger("setup_filters");
	},

	setup_filters: function (frm) {
		let filters = {};

		if (frm.doc.accounting_dimension) {
			nts .model.with_doctype(frm.doc.accounting_dimension, function () {
				if (nts .model.is_tree(frm.doc.accounting_dimension)) {
					filters["is_group"] = 0;
				}

				if (nts .meta.has_field(frm.doc.accounting_dimension, "company")) {
					filters["company"] = frm.doc.company;
				}

				frm.set_query("dimension_value", "dimensions", function () {
					return {
						filters: filters,
					};
				});
			});
		}
	},

	accounting_dimension: function (frm) {
		frm.clear_table("dimensions");
		let row = frm.add_child("dimensions");
		row.accounting_dimension = frm.doc.accounting_dimension;
		frm.fields_dict["dimensions"].grid.update_docfield_property(
			"dimension_value",
			"label",
			frm.doc.accounting_dimension
		);
		frm.refresh_field("dimensions");
		frm.trigger("setup_filters");
	},
	apply_restriction_on_values: function (frm) {
		/** If restriction on values is not applied, we should set "allow_or_restrict" to "Restrict" with an empty allowed dimension table.
		 * Hence it's not "restricted" on any value.
		 */
		if (!frm.doc.apply_restriction_on_values) {
			frm.set_value("allow_or_restrict", "Restrict");
			frm.clear_table("dimensions");
			frm.refresh_field("dimensions");
		}
	},
});

nts .ui.form.on("Allowed Dimension", {
	dimensions_add: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.accounting_dimension = frm.doc.accounting_dimension;
		frm.refresh_field("dimensions");
	},
});
