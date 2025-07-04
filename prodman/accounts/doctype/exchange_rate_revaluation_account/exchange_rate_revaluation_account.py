# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts .model.document import Document


class ExchangeRateRevaluationAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		account: DF.Link
		account_currency: DF.Link | None
		balance_in_account_currency: DF.Currency
		balance_in_base_currency: DF.Currency
		current_exchange_rate: DF.Float
		gain_loss: DF.Currency
		new_balance_in_account_currency: DF.Currency
		new_balance_in_base_currency: DF.Currency
		new_exchange_rate: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		party: DF.DynamicLink | None
		party_type: DF.Link | None
		zero_balance: DF.Check
	# end: auto-generated types

	pass
