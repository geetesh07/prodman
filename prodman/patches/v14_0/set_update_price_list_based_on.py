import nts
from nts.utils import cint


def execute():
	nts.db.set_single_value(
		"Stock Settings",
		"update_price_list_based_on",
		(
			"Price List Rate"
			if cint(nts.db.get_single_value("Selling Settings", "editable_price_list_rate"))
			else "Rate"
		),
	)
