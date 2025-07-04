# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from nts.model.document import Document


class LandedCostPurchaseReceipt(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		grand_total: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		posting_date: DF.Date | None
		receipt_document: DF.DynamicLink
		receipt_document_type: DF.Literal["", "Purchase Invoice", "Purchase Receipt"]
		supplier: DF.Link | None
	# end: auto-generated types

	pass
