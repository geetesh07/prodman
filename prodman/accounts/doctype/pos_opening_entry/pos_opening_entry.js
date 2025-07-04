// Copyright (c) 2020, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .ui.form.on("POS Opening Entry", {
	setup(frm) {
		if (frm.doc.docstatus == 0) {
			frm.trigger("set_posting_date_read_only");
			frm.set_value("period_start_date", nts .datetime.now_datetime());
			frm.set_value("user", nts .session.user);
		}

		frm.set_query("user", function (doc) {
			return {
				query: "prodman.accounts.doctype.pos_closing_entry.pos_closing_entry.get_cashiers",
				filters: { parent: doc.pos_profile },
			};
		});
	},

	refresh(frm) {
		// set default posting date / time
		if (frm.doc.docstatus == 0) {
			if (!frm.doc.posting_date) {
				frm.set_value("posting_date", nts .datetime.nowdate());
			}
			frm.trigger("set_posting_date_read_only");
		}
	},

	set_posting_date_read_only(frm) {
		if (frm.doc.docstatus == 0 && frm.doc.set_posting_date) {
			frm.set_df_property("posting_date", "read_only", 0);
		} else {
			frm.set_df_property("posting_date", "read_only", 1);
		}
	},

	set_posting_date(frm) {
		frm.trigger("set_posting_date_read_only");
	},

	pos_profile: (frm) => {
		if (frm.doc.pos_profile) {
			nts .db.get_doc("POS Profile", frm.doc.pos_profile).then(({ payments }) => {
				if (payments.length) {
					frm.doc.balance_details = [];
					payments.forEach(({ mode_of_payment }) => {
						frm.add_child("balance_details", { mode_of_payment });
					});
					frm.refresh_field("balance_details");
				}
			});
		}
	},
});
