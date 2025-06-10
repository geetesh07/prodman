# Copyright (c) 2020, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("support", "doctype", "sla_fulfilled_on_status")
	nts.reload_doc("support", "doctype", "service_level_agreement")
	if nts.db.has_column("Service Level Agreement", "enable"):
		rename_field("Service Level Agreement", "enable", "enabled")

	for sla in nts.get_all("Service Level Agreement"):
		agreement = nts.get_doc("Service Level Agreement", sla.name)
		agreement.db_set("document_type", "Issue")
		agreement.reload()
		agreement.apply_sla_for_resolution = 1
		agreement.append("sla_fulfilled_on", {"status": "Resolved"})
		agreement.append("sla_fulfilled_on", {"status": "Closed"})
		agreement.save()
