# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class SubscriptionSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		cancel_after_grace: DF.Check
		grace_period: DF.Int
		prorate: DF.Check
	# end: auto-generated types

	pass
