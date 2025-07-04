# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class SalesInvoiceTimesheet(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		activity_type: DF.Link | None
		billing_amount: DF.Currency
		billing_hours: DF.Float
		description: DF.SmallText | None
		from_time: DF.Datetime | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project_name: DF.Data | None
		time_sheet: DF.Link | None
		timesheet_detail: DF.Data | None
		to_time: DF.Datetime | None
	# end: auto-generated types

	pass
