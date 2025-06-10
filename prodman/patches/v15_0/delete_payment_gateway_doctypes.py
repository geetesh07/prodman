import nts


def execute():
	for dt in ("GoCardless Settings", "GoCardless Mandate", "Mpesa Settings"):
		nts.delete_doc("DocType", dt, ignore_missing=True)
