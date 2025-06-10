import nts
from nts.utils import cint


def execute():
	nts.reload_doc("prodman_integrations", "doctype", "woocommerce_settings")
	doc = nts.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
