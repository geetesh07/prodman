import nts


def execute():
	if nts.db.exists("Page", "point-of-sale"):
		nts.rename_doc("Page", "pos", "point-of-sale", 1, 1)
