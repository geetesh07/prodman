// Copyright (c) 2016, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Gross and Net Profit Report"] = $.extend({}, prodman.financial_statements);

nts .query_reports["Gross and Net Profit Report"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
});
