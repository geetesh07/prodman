# Copyright (c) 2019, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import nts 
from nts .model.document import Document


class DiscountedInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		customer: DF.Link | None
		debit_to: DF.Link | None
		outstanding_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		posting_date: DF.Date | None
		sales_invoice: DF.Link
	# end: auto-generated types

	pass
