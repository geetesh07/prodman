# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


"""Global Defaults"""
import nts
import nts.defaults
from nts.custom.doctype.property_setter.property_setter import make_property_setter
from nts.utils import cint

keydict = {
	# "key in defaults": "key in Global Defaults"
	"company": "default_company",
	"currency": "default_currency",
	"country": "country",
	"hide_currency_symbol": "hide_currency_symbol",
	"account_url": "account_url",
	"disable_rounded_total": "disable_rounded_total",
	"disable_in_words": "disable_in_words",
}

from nts.model.document import Document


class GlobalDefaults(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		country: DF.Link | None
		default_company: DF.Link | None
		default_currency: DF.Link
		default_distance_unit: DF.Link | None
		demo_company: DF.Link | None
		disable_in_words: DF.Check
		disable_rounded_total: DF.Check
		hide_currency_symbol: DF.Literal["", "No", "Yes"]
	# end: auto-generated types

	def on_update(self):
		"""update defaults"""
		for key in keydict:
			nts.db.set_default(key, self.get(keydict[key], ""))

		# enable default currency
		if self.default_currency:
			nts.db.set_value("Currency", self.default_currency, "enabled", 1)

		self.toggle_rounded_total()
		self.toggle_in_words()

		nts.clear_cache()

	@nts.whitelist()
	def get_defaults(self):
		return nts.defaults.get_defaults()

	def toggle_rounded_total(self):
		self.disable_rounded_total = cint(self.disable_rounded_total)

		# Make property setters to hide rounded total fields
		for doctype in (
			"Quotation",
			"Sales Order",
			"Sales Invoice",
			"Delivery Note",
			"Supplier Quotation",
			"Purchase Order",
			"Purchase Invoice",
			"Purchase Receipt",
		):
			make_property_setter(
				doctype,
				"base_rounded_total",
				"hidden",
				self.disable_rounded_total,
				"Check",
				validate_fields_for_doctype=False,
			)
			make_property_setter(
				doctype, "base_rounded_total", "print_hide", 1, "Check", validate_fields_for_doctype=False
			)

			make_property_setter(
				doctype,
				"rounded_total",
				"hidden",
				self.disable_rounded_total,
				"Check",
				validate_fields_for_doctype=False,
			)
			make_property_setter(
				doctype,
				"rounded_total",
				"print_hide",
				self.disable_rounded_total,
				"Check",
				validate_fields_for_doctype=False,
			)

			make_property_setter(
				doctype,
				"disable_rounded_total",
				"default",
				cint(self.disable_rounded_total),
				"Text",
				validate_fields_for_doctype=False,
			)

	def toggle_in_words(self):
		self.disable_in_words = cint(self.disable_in_words)

		# Make property setters to hide in words fields
		for doctype in (
			"Quotation",
			"Sales Order",
			"Sales Invoice",
			"Delivery Note",
			"Supplier Quotation",
			"Purchase Order",
			"Purchase Invoice",
			"Purchase Receipt",
		):
			make_property_setter(
				doctype,
				"in_words",
				"hidden",
				self.disable_in_words,
				"Check",
				validate_fields_for_doctype=False,
			)
			make_property_setter(
				doctype,
				"in_words",
				"print_hide",
				self.disable_in_words,
				"Check",
				validate_fields_for_doctype=False,
			)
