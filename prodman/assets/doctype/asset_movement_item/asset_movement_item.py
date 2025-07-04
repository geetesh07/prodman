# Copyright (c) 2019, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts 
from nts .model.document import Document


class AssetMovementItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		asset: DF.Link
		asset_name: DF.Data | None
		company: DF.Link | None
		from_employee: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		source_location: DF.Link | None
		target_location: DF.Link | None
		to_employee: DF.Link | None
	# end: auto-generated types

	pass
