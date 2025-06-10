import nts


def execute():
	doctypes = nts.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	nts.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
