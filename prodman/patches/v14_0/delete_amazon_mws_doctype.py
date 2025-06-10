import nts


def execute():
	nts.delete_doc("DocType", "Amazon MWS Settings", ignore_missing=True)
