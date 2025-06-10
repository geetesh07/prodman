import nts

from prodman.setup.setup_wizard.operations.install_fixtures import add_sale_stages


def execute():
	nts.reload_doc("crm", "doctype", "sales_stage")

	nts.local.lang = nts.db.get_default("lang") or "en"

	add_sale_stages()
