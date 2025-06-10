import nts


def execute():
	nts.reload_doctype("Opportunity")
	if nts.db.has_column("Opportunity", "enquiry_from"):
		nts.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if nts.db.has_column("Opportunity", "lead") and nts.db.has_column("Opportunity", "enquiry_from"):
		nts.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if nts.db.has_column("Opportunity", "customer") and nts.db.has_column(
		"Opportunity", "enquiry_from"
	):
		nts.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
