# Copyright (c) 2021, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import nts 
from nts .model.document import Document


class AssetCapitalizationAssetItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		asset: DF.Link
		asset_name: DF.Data | None
		asset_value: DF.Currency
		cost_center: DF.Link | None
		current_asset_value: DF.Currency
		finance_book: DF.Link | None
		fixed_asset_account: DF.Link | None
		item_code: DF.Link
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
