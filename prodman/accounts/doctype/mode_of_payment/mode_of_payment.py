# Copyright (c) 2015, nts  Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts 
from nts  import _
from nts .model.document import Document


class ModeofPayment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.mode_of_payment_account.mode_of_payment_account import (
			ModeofPaymentAccount,
		)

		accounts: DF.Table[ModeofPaymentAccount]
		enabled: DF.Check
		mode_of_payment: DF.Data
		type: DF.Literal["Cash", "Bank", "General", "Phone"]
	# end: auto-generated types

	def validate(self):
		self.validate_accounts()
		self.validate_repeating_companies()
		self.validate_pos_mode_of_payment()

	def validate_repeating_companies(self):
		"""Error when Same Company is entered multiple times in accounts"""
		accounts_list = []
		for entry in self.accounts:
			accounts_list.append(entry.company)

		if len(accounts_list) != len(set(accounts_list)):
			nts .throw(_("Same Company is entered more than once"))

	def validate_accounts(self):
		for entry in self.accounts:
			"""Error when Company of Ledger account doesn't match with Company Selected"""
			if nts .get_cached_value("Account", entry.default_account, "company") != entry.company:
				nts .throw(
					_("Account {0} does not match with Company {1} in Mode of Account: {2}").format(
						entry.default_account, entry.company, self.name
					)
				)

	def validate_pos_mode_of_payment(self):
		if not self.enabled:
			pos_profiles = nts .db.sql(
				"""SELECT sip.parent FROM `tabSales Invoice Payment` sip
				WHERE sip.parenttype = 'POS Profile' and sip.mode_of_payment = %s""",
				(self.name),
			)
			pos_profiles = list(map(lambda x: x[0], pos_profiles))

			if pos_profiles:
				message = _(
					"POS Profile {} contains Mode of Payment {}. Please remove them to disable this mode."
				).format(nts .bold(", ".join(pos_profiles)), nts .bold(str(self.name)))
				nts .throw(message, title=_("Not Allowed"))
