import nts

from prodman.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	nts.reload_doc("crm", "doctype", "market_segment")

	nts.local.lang = nts.db.get_default("lang") or "en"

	add_market_segments()
