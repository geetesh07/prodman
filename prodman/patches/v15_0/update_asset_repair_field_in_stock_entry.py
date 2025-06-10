import nts
from nts.query_builder import DocType


def execute():
	if nts.db.has_column("Asset Repair", "stock_entry"):
		AssetRepair = DocType("Asset Repair")
		StockEntry = DocType("Stock Entry")

		(
			nts.qb.update(StockEntry)
			.join(AssetRepair)
			.on(StockEntry.name == AssetRepair.stock_entry)
			.set(StockEntry.asset_repair, AssetRepair.name)
		).run()
