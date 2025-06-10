import nts


def execute():
	asset = nts.qb.DocType("Asset")
	nts.qb.update(asset).set(asset.asset_quantity, 1).where(asset.asset_quantity == 0).run()
