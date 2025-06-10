nts.provide("prodman.demo");

$(document).on("toolbar_setup", function () {
	if (nts.boot.sysdefaults.demo_company) {
		render_clear_demo_action();
	}
});

function render_clear_demo_action() {
	let demo_action = $(
		`<a class="dropdown-item" onclick="return prodman.demo.clear_demo()">
			${__("Clear Demo Data")}
		</a>`
	);

	demo_action.appendTo($("#toolbar-user"));
}

prodman.demo.clear_demo = function () {
	nts.confirm(__("Are you sure you want to clear all demo data?"), () => {
		nts.call({
			method: "prodman.setup.demo.clear_demo_data",
			freeze: true,
			freeze_message: __("Clearing Demo Data..."),
			callback: function (r) {
				nts.ui.toolbar.clear_cache();
				nts.show_alert({
					message: __("Demo data cleared"),
					indicator: "green",
				});
			},
		});
	});
};
