# Copyright (c) 2023, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import nts 
from nts .model.document import Document


class RepostAccountingLedgerItems(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		voucher_no: DF.DynamicLink | None
		voucher_type: DF.Link | None
	# end: auto-generated types

	pass
