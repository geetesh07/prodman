# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document


class DeliverySettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		dispatch_attachment: DF.Link | None
		dispatch_template: DF.Link | None
		send_with_attachment: DF.Check
		stop_delay: DF.Int
	# end: auto-generated types

	pass
