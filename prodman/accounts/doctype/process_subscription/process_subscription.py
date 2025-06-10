# Copyright (c) 2023, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts 
from nts .model.document import Document
from nts .utils import getdate

from prodman.accounts.doctype.subscription.subscription import DateTimeLikeObject, process_all


class ProcessSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		amended_from: DF.Link | None
		posting_date: DF.Date
		subscription: DF.Link | None
	# end: auto-generated types

	def on_submit(self):
		process_all(subscription=self.subscription, posting_date=self.posting_date)


def create_subscription_process(
	subscription: str | None = None, posting_date: DateTimeLikeObject | None = None
):
	"""Create a new Process Subscription document"""
	doc = nts .new_doc("Process Subscription")
	doc.subscription = subscription
	doc.posting_date = getdate(posting_date)
	doc.submit()
