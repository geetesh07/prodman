# Copyright (c) 2018, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts

from prodman.setup.doctype.company.company import install_country_fixtures


def execute():
	nts.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in nts.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
