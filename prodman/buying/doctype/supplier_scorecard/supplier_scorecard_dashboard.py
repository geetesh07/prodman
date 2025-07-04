from nts import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _("This covers all scorecards tied to this Setup"),
		"fieldname": "supplier",
		"method": "prodman.buying.doctype.supplier_scorecard.supplier_scorecard.get_timeline_data",
		"transactions": [{"label": _("Scorecards"), "items": ["Supplier Scorecard Period"]}],
	}
