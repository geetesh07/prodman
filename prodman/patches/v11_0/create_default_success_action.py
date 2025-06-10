import nts

from prodman.setup.install import create_default_success_action


def execute():
	nts.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
