# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from nts .model.document import Document


class Bank(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.bank_transaction_mapping.bank_transaction_mapping import (
			BankTransactionMapping,
		)

		bank_name: DF.Data
		bank_transaction_mapping: DF.Table[BankTransactionMapping]
		plaid_access_token: DF.Data | None
		swift_number: DF.Data | None
		website: DF.Data | None
	# end: auto-generated types

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def on_trash(self):
		delete_contact_and_address("Bank", self.name)
