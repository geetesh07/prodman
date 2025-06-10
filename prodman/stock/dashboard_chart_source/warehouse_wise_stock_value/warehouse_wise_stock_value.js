nts.provide("nts.dashboards.chart_sources");

nts.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "prodman.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
		},
	],
};
