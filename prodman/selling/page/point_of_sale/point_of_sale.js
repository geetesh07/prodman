nts.provide("prodman.PointOfSale");

nts.pages["point-of-sale"].on_page_load = function (wrapper) {
	nts.ui.make_app_page({
		parent: wrapper,
		title: __("Point of Sale"),
		single_column: true,
	});

	nts.require("point-of-sale.bundle.js", function () {
		wrapper.pos = new prodman.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

nts.pages["point-of-sale"].refresh = function (wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};
