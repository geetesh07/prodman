import functools
import inspect

import nts
from nts.utils.user import is_website_user

__version__ = "15.64.1"


def get_default_company(user=None):
	"""Get default company for user"""
	from nts.defaults import get_user_default_as_list

	if not user:
		user = nts.session.user

	companies = get_user_default_as_list("company", user)
	if companies:
		default_company = companies[0]
	else:
		default_company = nts.db.get_single_value("Global Defaults", "default_company")

	return default_company


def get_default_currency():
	"""Returns the currency of the default company"""
	company = get_default_company()
	if company:
		return nts.get_cached_value("Company", company, "default_currency")


def get_default_cost_center(company):
	"""Returns the default cost center of the company"""
	if not company:
		return None

	if not nts.flags.company_cost_center:
		nts.flags.company_cost_center = {}
	if company not in nts.flags.company_cost_center:
		nts.flags.company_cost_center[company] = nts.get_cached_value("Company", company, "cost_center")
	return nts.flags.company_cost_center[company]


def get_company_currency(company):
	"""Returns the default company currency"""
	if not nts.flags.company_currency:
		nts.flags.company_currency = {}
	if company not in nts.flags.company_currency:
		nts.flags.company_currency[company] = nts.db.get_value(
			"Company", company, "default_currency", cache=True
		)
	return nts.flags.company_currency[company]


def set_perpetual_inventory(enable=1, company=None):
	if not company:
		company = "_Test Company" if nts.flags.in_test else get_default_company()

	company = nts.get_doc("Company", company)
	company.enable_perpetual_inventory = enable
	company.save()


def encode_company_abbr(name, company=None, abbr=None):
	"""Returns name encoded with company abbreviation"""
	company_abbr = abbr or nts.get_cached_value("Company", company, "abbr")
	parts = name.rsplit(" - ", 1)

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)


def is_perpetual_inventory_enabled(company):
	if not company:
		company = "_Test Company" if nts.flags.in_test else get_default_company()

	if not hasattr(nts.local, "enable_perpetual_inventory"):
		nts.local.enable_perpetual_inventory = {}

	if company not in nts.local.enable_perpetual_inventory:
		nts.local.enable_perpetual_inventory[company] = (
			nts.get_cached_value("Company", company, "enable_perpetual_inventory") or 0
		)

	return nts.local.enable_perpetual_inventory[company]


def get_default_finance_book(company=None):
	if not company:
		company = get_default_company()

	if not hasattr(nts.local, "default_finance_book"):
		nts.local.default_finance_book = {}

	if company not in nts.local.default_finance_book:
		nts.local.default_finance_book[company] = nts.get_cached_value(
			"Company", company, "default_finance_book"
		)

	return nts.local.default_finance_book[company]


def get_party_account_type(party_type):
	if not hasattr(nts.local, "party_account_types"):
		nts.local.party_account_types = {}

	if party_type not in nts.local.party_account_types:
		nts.local.party_account_types[party_type] = (
			nts.db.get_value("Party Type", party_type, "account_type") or ""
		)

	return nts.local.party_account_types[party_type]


def get_region(company=None):
	"""Return the default country based on flag, company or global settings

	You can also set global company flag in `nts.flags.company`
	"""

	if not company:
		company = nts.local.flags.company

	if company:
		return nts.get_cached_value("Company", company, "country")

	return nts.flags.country or nts.get_system_settings("country")


def allow_regional(fn):
	"""Decorator to make a function regionally overridable

	Example:
	@prodman.allow_regional
	def myfunction():
	  pass"""

	@functools.wraps(fn)
	def caller(*args, **kwargs):
		overrides = nts.get_hooks("regional_overrides", {}).get(get_region())
		function_path = f"{inspect.getmodule(fn).__name__}.{fn.__name__}"

		if not overrides or function_path not in overrides:
			return fn(*args, **kwargs)

		# Priority given to last installed app
		return nts.get_attr(overrides[function_path][-1])(*args, **kwargs)

	return caller


def check_app_permission():
	if nts.session.user == "Administrator":
		return True

	if is_website_user():
		return False

	return True
