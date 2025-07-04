import nts


def execute():
	asset = nts.qb.DocType("Asset")
	nts.qb.update(asset).set(asset.total_asset_cost, asset.gross_purchase_amount).run()

	asset_repair_list = nts.db.get_all(
		"Asset Repair",
		filters={"docstatus": 1, "repair_status": "Completed", "capitalize_repair_cost": 1},
		fields=["asset", "repair_cost"],
	)

	for asset_repair in asset_repair_list:
		nts.qb.update(asset).set(
			asset.total_asset_cost, asset.total_asset_cost + asset_repair.repair_cost
		).where(asset.name == asset_repair.asset).run()
