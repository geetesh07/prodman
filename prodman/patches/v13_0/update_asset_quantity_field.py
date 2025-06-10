import nts


def execute():
	if nts.db.count("Asset"):
		nts.reload_doc("assets", "doctype", "Asset")
		asset = nts.qb.DocType("Asset")
		nts.qb.update(asset).set(asset.asset_quantity, 1).run()
