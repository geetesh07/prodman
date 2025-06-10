// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.query_reports["Sales Order Trends"] = $.extend({}, prodman.sales_trends_filters);

nts.query_reports["Sales Order Trends"]["filters"].push({
	fieldname: "include_closed_orders",
	label: __("Include Closed Orders"),
	fieldtype: "Check",
	default: 0,
});
