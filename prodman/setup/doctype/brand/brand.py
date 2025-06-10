# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import copy

import nts
from nts.model.document import Document


class Brand(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.stock.doctype.item_default.item_default import ItemDefault

		brand: DF.Data
		brand_defaults: DF.Table[ItemDefault]
		description: DF.Text | None
		image: DF.AttachImage | None
	# end: auto-generated types

	pass


def get_brand_defaults(item, company):
	item = nts.get_cached_doc("Item", item)
	if item.brand:
		brand = nts.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = copy.deepcopy(d.as_dict())
				row.pop("name")
				return row

	return nts._dict()
