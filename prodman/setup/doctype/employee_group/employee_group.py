# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class EmployeeGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.setup.doctype.employee_group_table.employee_group_table import EmployeeGroupTable

		employee_group_name: DF.Data
		employee_list: DF.Table[EmployeeGroupTable]
	# end: auto-generated types

	pass
