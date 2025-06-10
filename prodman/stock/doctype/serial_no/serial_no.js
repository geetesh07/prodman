// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch("customer", "customer_name", "customer_name");
cur_frm.add_fetch("supplier", "supplier_name", "supplier_name");

cur_frm.add_fetch("item_code", "item_name", "item_name");
cur_frm.add_fetch("item_code", "description", "description");
cur_frm.add_fetch("item_code", "item_group", "item_group");
cur_frm.add_fetch("item_code", "brand", "brand");

cur_frm.cscript.onload = function () {
	cur_frm.set_query("item_code", function () {
		return prodman.queries.item({ is_stock_item: 1, has_serial_no: 1 });
	});
};

nts.ui.form.on("Serial No", "refresh", function (frm) {
	frm.toggle_enable("item_code", frm.doc.__islocal);
});

nts.ui.form.on("Serial No", {
	refresh(frm) {
		frm.trigger("view_ledgers");
	},

	view_ledgers(frm) {
		frm.add_custom_button(__("View Ledgers"), () => {
			nts.route_options = {
				item_code: frm.doc.item_code,
				serial_no: frm.doc.name,
				posting_date: nts.datetime.now_date(),
				posting_time: nts.datetime.now_time(),
			};
			nts.set_route("query-report", "Serial No Ledger");
		}).addClass("btn-primary");
	},
});
