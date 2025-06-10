import nts


def execute():
	nts.reload_doc("setup", "doctype", "uom")

	uom = nts.qb.DocType("UOM")

	(
		nts.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
