# Copyright (c) 2023, nts Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import nts


def execute():
	navbar_settings = nts.get_single("Navbar Settings")
	for item in navbar_settings.help_dropdown:
		if item.is_standard and item.route == "https://prodman.com/docs/user/manual":
			item.route = "https://docs.prodman.com/docs/v14/user/manual/en/introduction"

	navbar_settings.save()
