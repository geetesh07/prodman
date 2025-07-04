# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class EmployeeGroupTable(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		employee: DF.Link | None
		employee_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		user_id: DF.Data | None
	# end: auto-generated types

	pass
