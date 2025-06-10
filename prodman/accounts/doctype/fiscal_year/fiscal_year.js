// Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts .ui.form.on("Fiscal Year", {
	onload: function (frm) {
		if (frm.doc.__islocal) {
			frm.set_value("year_start_date", nts .datetime.year_start());
		}
	},
	year_start_date: function (frm) {
		if (!frm.doc.is_short_year) {
			let year_end_date = nts .datetime.add_days(
				nts .datetime.add_months(frm.doc.year_start_date, 12),
				-1
			);
			frm.set_value("year_end_date", year_end_date);
		}
	},
});
