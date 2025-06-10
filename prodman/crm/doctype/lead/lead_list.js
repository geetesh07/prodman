nts.listview_settings["Lead"] = {
	get_indicator: function (doc) {
		var indicator = [__(doc.status), nts.utils.guess_colour(doc.status), "status,=," + doc.status];
		return indicator;
	},
	onload: function (listview) {
		if (nts.boot.user.can_create.includes("Prospect")) {
			listview.page.add_action_item(__("Create Prospect"), function () {
				nts.model.with_doctype("Prospect", function () {
					let prospect = nts.model.get_new_doc("Prospect");
					let leads = listview.get_checked_items();
					nts.db.get_value(
						"Lead",
						leads[0].name,
						[
							"company_name",
							"no_of_employees",
							"industry",
							"market_segment",
							"territory",
							"fax",
							"website",
							"lead_owner",
						],
						(r) => {
							prospect.company_name = r.company_name;
							prospect.no_of_employees = r.no_of_employees;
							prospect.industry = r.industry;
							prospect.market_segment = r.market_segment;
							prospect.territory = r.territory;
							prospect.fax = r.fax;
							prospect.website = r.website;
							prospect.prospect_owner = r.lead_owner;

							leads.forEach(function (lead) {
								let lead_prospect_row = nts.model.add_child(prospect, "leads");
								lead_prospect_row.lead = lead.name;
							});
							nts.set_route("Form", "Prospect", prospect.name);
						}
					);
				});
			});
		}
	},
};
