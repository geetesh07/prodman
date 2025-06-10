# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
import plaid
import requests
from nts import _
from plaid.errors import APIError, InvalidRequestError, ItemError


class PlaidConnector:
	def __init__(self, access_token=None):
		self.access_token = access_token
		self.settings = nts.get_single("Plaid Settings")
		self.products = ["transactions"]
		self.client_name = nts.local.site
		self.client = plaid.Client(
			client_id=self.settings.plaid_client_id,
			secret=self.settings.get_password("plaid_secret"),
			environment=self.settings.plaid_env,
			api_version="2020-09-14",
		)

	def get_access_token(self, public_token):
		if public_token is None:
			nts.log_error("Plaid: Public token is missing")
		response = self.client.Item.public_token.exchange(public_token)
		access_token = response["access_token"]
		return access_token

	def get_token_request(self, update_mode=False):
		country_codes = (
			["US", "CA", "FR", "IE", "NL", "ES", "GB"]
			if self.settings.enable_european_access
			else ["US", "CA"]
		)
		args = {
			"client_name": self.client_name,
			# only allow Plaid-supported languages and countries (LAST: Sep-19-2020)
			"language": nts.local.lang if nts.local.lang in ["en", "fr", "es", "nl"] else "en",
			"country_codes": country_codes,
			"user": {"client_user_id": nts.generate_hash(nts.session.user, length=32)},
		}

		if update_mode:
			args["access_token"] = self.access_token
		else:
			args.update(
				{
					"client_id": self.settings.plaid_client_id,
					"secret": self.settings.plaid_secret,
					"products": self.products,
				}
			)

		return args

	def get_link_token(self, update_mode=False):
		token_request = self.get_token_request(update_mode)

		try:
			response = self.client.LinkToken.create(token_request)
		except InvalidRequestError:
			nts.log_error("Plaid: Invalid request error")
			nts.msgprint(_("Please check your Plaid client ID and secret values"))
		except APIError as e:
			nts.log_error("Plaid: Authentication error")
			nts.throw(_(str(e)), title=_("Authentication Failed"))
		else:
			return response["link_token"]

	def get_transactions(self, start_date, end_date, account_id=None):
		kwargs = dict(access_token=self.access_token, start_date=start_date, end_date=end_date)
		if account_id:
			kwargs.update(dict(account_ids=[account_id]))

		try:
			response = self.client.Transactions.get(**kwargs)
			transactions = response["transactions"]
			while len(transactions) < response["total_transactions"]:
				response = self.client.Transactions.get(
					self.access_token, start_date=start_date, end_date=end_date, offset=len(transactions)
				)
				transactions.extend(response["transactions"])
			return transactions
		except ItemError as e:
			raise e
		except Exception:
			nts.log_error("Plaid: Transactions sync error")
