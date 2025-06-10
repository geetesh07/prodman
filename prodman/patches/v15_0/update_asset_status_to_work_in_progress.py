import nts


def execute():
	Asset = nts.qb.DocType("Asset")
	query = (
		nts.qb.update(Asset)
		.set(Asset.status, "Work In Progress")
		.where((Asset.docstatus == 0) & (Asset.is_composite_asset == 1))
	)
	query.run()
