// Copyright (c) 2020, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Video", {
	refresh: function (frm) {
		frm.events.toggle_youtube_statistics_section(frm);
		frm.add_custom_button(__("Watch Video"), () => nts.help.show_video(frm.doc.url, frm.doc.title));
	},

	toggle_youtube_statistics_section: (frm) => {
		if (frm.doc.provider === "YouTube") {
			nts.db.get_single_value("Video Settings", "enable_youtube_tracking").then((val) => {
				frm.toggle_display("youtube_tracking_section", val);
			});
		}
	},
});
