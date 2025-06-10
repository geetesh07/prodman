import nts


# not able to use nts.qb because of this bug https://github.com/nts/nts/issues/20292
def execute():
	if nts.db.has_column("Asset Repair", "warehouse"):
		# nosemgrep
		nts.db.sql(
			"""UPDATE `tabAsset Repair Consumed Item` ar_item
			JOIN `tabAsset Repair` ar
			ON ar.name = ar_item.parent
			SET ar_item.warehouse = ar.warehouse
			WHERE ifnull(ar.warehouse, '') != ''"""
		)
