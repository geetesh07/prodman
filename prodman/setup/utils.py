# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import nts
from nts import _
from nts.utils import add_days, flt, get_datetime_str, nowdate
from nts.utils.data import getdate, now_datetime
from nts.utils.nestedset import get_root_of

from prodman import get_default_company

PEGGED_CURRENCIES = {
	"USD": {"AED": 3.6725},  # AED is pegged to USD at a rate of 3.6725 since 1997
}


def before_tests():
	nts.clear_cache()
	# complete setup if missing
	from nts.desk.page.setup_wizard.setup_wizard import setup_complete

	if not nts.db.a_row_exists("Company"):
		current_year = now_datetime().year
		setup_complete(
			{
				"currency": "USD",
				"full_name": "Test User",
				"company_name": "Wind Power LLC",
				"timezone": "America/New_York",
				"company_abbr": "WP",
				"industry": "Manufacturing",
				"country": "United States",
				"fy_start_date": f"{current_year}-01-01",
				"fy_end_date": f"{current_year}-12-31",
				"language": "english",
				"company_tagline": "Testing",
				"email": "test@prodman.com",
				"password": "test",
				"chart_of_accounts": "Standard",
			}
		)

	nts.db.sql("delete from `tabItem Price`")

	_enable_all_roles_for_admin()

	set_defaults_for_tests()

	nts.db.commit()


def get_pegged_rate(from_currency: str, to_currency: str, transaction_date) -> float | None:
	if rate := PEGGED_CURRENCIES.get(from_currency, {}).get(to_currency):
		return rate
	elif rate := PEGGED_CURRENCIES.get(to_currency, {}).get(from_currency):
		return 1 / rate
	return None


@nts.whitelist()
def get_exchange_rate(from_currency, to_currency, transaction_date=None, args=None):
	if not (from_currency and to_currency):
		# manqala 19/09/2016: Should this be an empty return or should it throw and exception?
		return
	if from_currency == to_currency:
		return 1

	if not transaction_date:
		transaction_date = nowdate()

	currency_settings = nts.get_doc("Accounts Settings").as_dict()
	allow_stale_rates = currency_settings.get("allow_stale")

	filters = [
		["date", "<=", get_datetime_str(transaction_date)],
		["from_currency", "=", from_currency],
		["to_currency", "=", to_currency],
	]

	if args == "for_buying":
		filters.append(["for_buying", "=", "1"])
	elif args == "for_selling":
		filters.append(["for_selling", "=", "1"])

	if not allow_stale_rates:
		stale_days = currency_settings.get("stale_days")
		checkpoint_date = add_days(transaction_date, -stale_days)
		filters.append(["date", ">", get_datetime_str(checkpoint_date)])

	# cksgb 19/09/2016: get last entry in Currency Exchange with from_currency and to_currency.
	entries = nts.get_all(
		"Currency Exchange", fields=["exchange_rate"], filters=filters, order_by="date desc", limit=1
	)
	if entries:
		return flt(entries[0].exchange_rate)

	if nts.get_cached_value("Currency Exchange Settings", "Currency Exchange Settings", "disabled"):
		return 0.00

	if rate := get_pegged_rate(from_currency, to_currency, transaction_date):
		return rate

	try:
		cache = nts.cache()
		key = f"currency_exchange_rate_{transaction_date}:{from_currency}:{to_currency}"
		value = cache.get(key)

		if not value:
			import requests

			settings = nts.get_cached_doc("Currency Exchange Settings")
			req_params = {
				"transaction_date": transaction_date,
				"from_currency": from_currency if from_currency != "AED" else "USD",
				"to_currency": to_currency if to_currency != "AED" else "USD",
			}
			params = {}
			for row in settings.req_params:
				params[row.key] = format_ces_api(row.value, req_params)
			response = requests.get(format_ces_api(settings.api_endpoint, req_params), params=params)
			# expire in 6 hours
			response.raise_for_status()
			value = response.json()
			for res_key in settings.result_key:
				value = value[format_ces_api(str(res_key.key), req_params)]
			cache.setex(name=key, time=21600, value=flt(value))

		# Support AED conversion through pegged USD
		value = flt(value)
		if to_currency == "AED":
			value *= 3.6725
		if from_currency == "AED":
			value /= 3.6725

		return flt(value)
	except Exception:
		nts.log_error("Unable to fetch exchange rate")
		nts.msgprint(
			_(
				"Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually"
			).format(from_currency, to_currency, transaction_date)
		)
		return 0.0


def format_ces_api(data, param):
	return data.format(
		transaction_date=param.get("transaction_date"),
		to_currency=param.get("to_currency"),
		from_currency=param.get("from_currency"),
	)


def enable_all_roles_and_domains():
	"""enable all roles and domain for testing"""
	_enable_all_roles_for_admin()


def _enable_all_roles_for_admin():
	from nts.desk.page.setup_wizard.setup_wizard import add_all_roles_to

	all_roles = set(nts.db.get_values("Role", pluck="name"))
	admin_roles = set(
		nts.db.get_values("Has Role", {"parent": "Administrator"}, fieldname="role", pluck="role")
	)

	if all_roles.difference(admin_roles):
		add_all_roles_to("Administrator")


def set_defaults_for_tests():
	defaults = {
		"customer_group": get_root_of("Customer Group"),
		"territory": get_root_of("Territory"),
	}
	nts.db.set_single_value("Selling Settings", defaults)
	for key, value in defaults.items():
		nts.db.set_default(key, value)
	nts.db.set_single_value("Stock Settings", "auto_insert_price_list_rate_if_missing", 0)


def insert_record(records):
	from nts.desk.page.setup_wizard.setup_wizard import make_records

	make_records(records)


def welcome_email():
	site_name = get_default_company() or "prodman"
	title = _("Welcome to {0}").format(site_name)
	return title
