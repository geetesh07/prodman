// Copyright (c) 2013, nts  Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts .query_reports["Cash Flow"] = $.extend(prodman.financial_statements, {
	name_field: "section",
	parent_field: "parent_section",
});

prodman.utils.add_dimensions("Cash Flow", 10);

// The last item in the array is the definition for Presentation Currency
// filter. It won't be used in cash flow for now so we pop it. Please take
// of this if you are working here.

nts .query_reports["Cash Flow"]["filters"].splice(8, 1);

nts .query_reports["Cash Flow"]["filters"].push({
	fieldname: "include_default_book_entries",
	label: __("Include Default FB Entries"),
	fieldtype: "Check",
	default: 1,
});
