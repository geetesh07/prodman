# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doctype("Quotation")
	nts.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	nts.db.sql(""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """)

	nts.reload_doctype("Opportunity")
	nts.db.sql(""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """)
	nts.db.sql(
		""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """
	)
