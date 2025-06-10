nts.listview_settings["Supplier Quotation"] = {
	add_fields: ["supplier", "base_grand_total", "status", "company", "currency"],
	get_indicator: function (doc) {
		if (doc.status === "Ordered") {
			return [__("Ordered"), "green", "status,=,Ordered"];
		} else if (doc.status === "Rejected") {
			return [__("Lost"), "gray", "status,=,Lost"];
		} else if (doc.status === "Expired") {
			return [__("Expired"), "gray", "status,=,Expired"];
		}
	},

	onload: function (listview) {
		if (nts.model.can_create("Purchase Order")) {
			listview.page.add_action_item(__("Purchase Order"), () => {
				prodman.bulk_transaction_processing.create(listview, "Supplier Quotation", "Purchase Order");
			});
		}

		if (nts.model.can_create("Purchase Invoice")) {
			listview.page.add_action_item(__("Purchase Invoice"), () => {
				prodman.bulk_transaction_processing.create(
					listview,
					"Supplier Quotation",
					"Purchase Invoice"
				);
			});
		}
	},
};
