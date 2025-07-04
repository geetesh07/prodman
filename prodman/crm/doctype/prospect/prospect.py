# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from nts.model.mapper import get_mapped_doc

from prodman.crm.utils import CRMNote, copy_comments, link_communications, link_open_events


class Prospect(CRMNote):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.crm.doctype.crm_note.crm_note import CRMNote
		from prodman.crm.doctype.prospect_lead.prospect_lead import ProspectLead
		from prodman.crm.doctype.prospect_opportunity.prospect_opportunity import ProspectOpportunity

		annual_revenue: DF.Currency
		company: DF.Link
		company_name: DF.Data | None
		customer_group: DF.Link | None
		fax: DF.Data | None
		industry: DF.Link | None
		leads: DF.Table[ProspectLead]
		market_segment: DF.Link | None
		no_of_employees: DF.Literal["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
		notes: DF.Table[CRMNote]
		opportunities: DF.Table[ProspectOpportunity]
		prospect_owner: DF.Link | None
		territory: DF.Link | None
		website: DF.Data | None
	# end: auto-generated types

	def onload(self):
		load_address_and_contact(self)

	def on_update(self):
		self.link_with_lead_contact_and_address()

	def on_trash(self):
		delete_contact_and_address(self.doctype, self.name)

	def after_insert(self):
		carry_forward_communication_and_comments = nts.db.get_single_value(
			"CRM Settings", "carry_forward_communication_and_comments"
		)

		for row in self.get("leads"):
			if carry_forward_communication_and_comments:
				copy_comments("Lead", row.lead, self)
				link_communications("Lead", row.lead, self)
			link_open_events("Lead", row.lead, self)

		for row in self.get("opportunities"):
			if carry_forward_communication_and_comments:
				copy_comments("Opportunity", row.opportunity, self)
				link_communications("Opportunity", row.opportunity, self)
			link_open_events("Opportunity", row.opportunity, self)

	def link_with_lead_contact_and_address(self):
		for row in self.leads:
			links = nts.get_all(
				"Dynamic Link",
				filters={"link_doctype": "Lead", "link_name": row.lead},
				fields=["parent", "parenttype"],
			)
			for link in links:
				linked_doc = nts.get_doc(link["parenttype"], link["parent"])
				exists = False

				for d in linked_doc.get("links"):
					if d.link_doctype == self.doctype and d.link_name == self.name:
						exists = True

				if not exists:
					linked_doc.append("links", {"link_doctype": self.doctype, "link_name": self.name})
					linked_doc.save(ignore_permissions=True)


@nts.whitelist()
def make_customer(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.customer_type = "Company"
		target.company_name = source.name
		target.customer_group = source.customer_group or nts.db.get_default("Customer Group")

	doclist = get_mapped_doc(
		"Prospect",
		source_name,
		{
			"Prospect": {
				"doctype": "Customer",
				"field_map": {"company_name": "customer_name", "currency": "default_currency", "fax": "fax"},
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=False,
	)

	return doclist


@nts.whitelist()
def make_opportunity(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.opportunity_from = "Prospect"
		target.customer_name = source.company_name
		target.customer_group = source.customer_group or nts.db.get_default("Customer Group")

	doclist = get_mapped_doc(
		"Prospect",
		source_name,
		{
			"Prospect": {
				"doctype": "Opportunity",
				"field_map": {"name": "party_name", "prospect_owner": "opportunity_owner"},
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=False,
	)

	return doclist


@nts.whitelist()
def get_opportunities(prospect):
	return nts.get_all(
		"Opportunity",
		filters={"opportunity_from": "Prospect", "party_name": prospect},
		fields=[
			"opportunity_owner",
			"sales_stage",
			"status",
			"expected_closing",
			"probability",
			"opportunity_amount",
			"currency",
			"contact_person",
			"contact_email",
			"contact_mobile",
			"creation",
			"name",
		],
	)
