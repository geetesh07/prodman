import nts

from prodman.setup.install import setup_currency_exchange


def execute():
	nts.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
