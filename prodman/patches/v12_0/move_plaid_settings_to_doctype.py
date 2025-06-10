# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("prodman_integrations", "doctype", "plaid_settings")
	plaid_settings = nts.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (nts.conf.plaid_client_id and nts.conf.plaid_env and nts.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": nts.conf.plaid_client_id,
					"plaid_env": nts.conf.plaid_env,
					"plaid_secret": nts.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
