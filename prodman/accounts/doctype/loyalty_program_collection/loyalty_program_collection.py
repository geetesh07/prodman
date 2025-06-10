# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class LoyaltyProgramCollection(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		collection_factor: DF.Currency
		min_spent: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		tier_name: DF.Data
	# end: auto-generated types

	pass
