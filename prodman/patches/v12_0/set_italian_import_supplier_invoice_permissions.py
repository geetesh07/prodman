# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts

from prodman.regional.italy.setup import add_permissions


def execute():
	countries = nts.get_all("Company", fields="country")
	countries = [country["country"] for country in countries]
	if "Italy" in countries:
		add_permissions()
