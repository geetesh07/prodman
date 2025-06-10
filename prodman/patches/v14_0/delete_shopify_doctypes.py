import nts


def execute():
	nts.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	nts.delete_doc("DocType", "Shopify Log", ignore_missing=True)
