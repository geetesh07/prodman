# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import nts
from nts.model.document import Document


class Competitor(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		competitor_name: DF.Data
		website: DF.Data | None
	# end: auto-generated types

	pass
