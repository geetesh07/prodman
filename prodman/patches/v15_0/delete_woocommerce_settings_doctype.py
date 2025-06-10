import nts


def execute():
	nts.delete_doc("DocType", "Woocommerce Settings", ignore_missing=True)
