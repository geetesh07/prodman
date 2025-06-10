# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt


from nts.model.document import Document


class WebsiteItemGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		item_group: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
