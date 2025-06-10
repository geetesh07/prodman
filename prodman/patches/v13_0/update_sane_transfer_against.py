import nts


def execute():
	bom = nts.qb.DocType("BOM")

	(
		nts.qb.update(bom).set(bom.transfer_material_against, "Work Order").where(bom.with_operations == 0)
	).run()
