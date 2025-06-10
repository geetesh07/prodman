// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.provide("prodman");

// preferred modules for breadcrumbs
$.extend(nts.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	Territory: "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	Brand: "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support",
});

$.extend(nts.breadcrumbs.module_map, {
	"prodman Integrations": "Integrations",
	Geo: "Settings",
	Portal: "Website",
	Utilities: "Settings",
	"E-commerce": "Website",
	Contacts: "CRM",
});
