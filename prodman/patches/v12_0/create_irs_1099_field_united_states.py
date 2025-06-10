import nts

from prodman.regional.united_states.setup import make_custom_fields


def execute():
	nts.reload_doc("accounts", "doctype", "allowed_to_transact_with", force=True)
	nts.reload_doc("accounts", "doctype", "pricing_rule_detail", force=True)
	nts.reload_doc("crm", "doctype", "lost_reason_detail", force=True)
	nts.reload_doc("setup", "doctype", "quotation_lost_reason_detail", force=True)

	company = nts.get_all("Company", filters={"country": "United States"})
	if not company:
		return

	make_custom_fields()
