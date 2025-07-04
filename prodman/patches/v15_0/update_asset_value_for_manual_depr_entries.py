import nts
from nts.query_builder.functions import IfNull, Sum


def execute():
	asset = nts.qb.DocType("Asset")
	gle = nts.qb.DocType("GL Entry")
	aca = nts.qb.DocType("Asset Category Account")
	company = nts.qb.DocType("Company")

	asset_total_depr_value_map = (
		nts.qb.from_(gle)
		.join(asset)
		.on(gle.against_voucher == asset.name)
		.join(aca)
		.on((aca.parent == asset.asset_category) & (aca.company_name == asset.company))
		.join(company)
		.on(company.name == asset.company)
		.select(Sum(gle.debit).as_("value"), asset.name.as_("asset_name"))
		.where(gle.account == IfNull(aca.depreciation_expense_account, company.depreciation_expense_account))
		.where(gle.debit != 0)
		.where(gle.is_cancelled == 0)
		.where(asset.docstatus == 1)
		.where(asset.calculate_depreciation == 0)
		.groupby(asset.name)
	)

	nts.qb.update(asset).join(asset_total_depr_value_map).on(
		asset_total_depr_value_map.asset_name == asset.name
	).set(
		asset.value_after_depreciation, asset.value_after_depreciation - asset_total_depr_value_map.value
	).where(asset.docstatus == 1).where(asset.calculate_depreciation == 0).run()
