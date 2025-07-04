// Copyright (c) 2019, nts Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

nts.ui.form.on("Website Theme", {
	validate(frm) {
		let theme_scss = frm.doc.theme_scss;
		if (
			theme_scss &&
			theme_scss.includes("nts/public/scss/website") &&
			!theme_scss.includes("prodman/public/scss/website")
		) {
			frm.set_value("theme_scss", `${frm.doc.theme_scss}\n@import "prodman/public/scss/website";`);
		}
	},
});
