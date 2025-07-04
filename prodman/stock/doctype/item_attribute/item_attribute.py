# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.utils import flt

from prodman.controllers.item_variant import (
	InvalidItemAttributeValueError,
	validate_is_incremental,
	validate_item_attribute_value,
)


class ItemAttributeIncrementError(nts.ValidationError):
	pass


class ItemAttribute(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.stock.doctype.item_attribute_value.item_attribute_value import ItemAttributeValue

		attribute_name: DF.Data
		disabled: DF.Check
		from_range: DF.Float
		increment: DF.Float
		item_attribute_values: DF.Table[ItemAttributeValue]
		numeric_values: DF.Check
		to_range: DF.Float
	# end: auto-generated types

	def __setup__(self):
		self.flags.ignore_these_exceptions_in_test = [InvalidItemAttributeValueError]

	def validate(self):
		nts.flags.attribute_values = None
		self.validate_numeric()
		self.validate_duplication()

	def on_update(self):
		self.validate_exising_items()
		self.set_enabled_disabled_in_items()

	def set_enabled_disabled_in_items(self):
		db_value = self.get_doc_before_save()
		if not db_value or db_value.disabled != self.disabled:
			item_variant_table = nts.qb.DocType("Item Variant Attribute")
			query = (
				nts.qb.update(item_variant_table)
				.set(item_variant_table.disabled, self.disabled)
				.where(item_variant_table.attribute == self.name)
			)

			query.run()

	def validate_exising_items(self):
		"""Validate that if there are existing items with attributes, they are valid"""
		attributes_list = [d.attribute_value for d in self.item_attribute_values]

		# Get Item Variant Attribute details of variant items
		items = nts.db.sql(
			"""
			select
				i.name, iva.attribute_value as value
			from
				`tabItem Variant Attribute` iva, `tabItem` i
			where
				iva.attribute = %(attribute)s
				and iva.parent = i.name and
				i.variant_of is not null and i.variant_of != ''""",
			{"attribute": self.name},
			as_dict=1,
		)

		for item in items:
			if self.numeric_values:
				validate_is_incremental(self, self.name, item.value, item.name)
			else:
				validate_item_attribute_value(
					attributes_list, self.name, item.value, item.name, from_variant=False
				)

	def validate_numeric(self):
		if self.numeric_values:
			self.set("item_attribute_values", [])
			if self.from_range is None or self.to_range is None:
				nts.throw(_("Please specify from/to range"))

			elif flt(self.from_range) >= flt(self.to_range):
				nts.throw(_("From Range has to be less than To Range"))

			if not self.increment:
				nts.throw(_("Increment cannot be 0"), ItemAttributeIncrementError)
		else:
			self.from_range = self.to_range = self.increment = 0

	def validate_duplication(self):
		values, abbrs = [], []
		for d in self.item_attribute_values:
			if d.attribute_value.lower() in map(str.lower, values):
				nts.throw(
					_("Attribute value: {0} must appear only once").format(d.attribute_value.title())
				)
			values.append(d.attribute_value)

			if d.abbr.lower() in map(str.lower, abbrs):
				nts.throw(_("Abbreviation: {0} must appear only once").format(d.abbr.title()))
			abbrs.append(d.abbr)
