nts.pages["visual-plant-floor"].on_page_load = function (wrapper) {
	var page = nts.ui.make_app_page({
		parent: wrapper,
		title: "Visual Plant Floor",
		single_column: true,
	});

	nts.visual_plant_floor = new nts.ui.VisualPlantFloor(
		{ wrapper: $(wrapper).find(".layout-main-section") },
		wrapper.page
	);
};
