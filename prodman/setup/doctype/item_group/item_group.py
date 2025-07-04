# Copyright (c) 2021, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import copy

import nts
from nts import _
from nts.utils.nestedset import NestedSet


class ItemGroup(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.stock.doctype.item_default.item_default import ItemDefault
		from prodman.stock.doctype.item_tax.item_tax import ItemTax

		image: DF.AttachImage | None
		is_group: DF.Check
		item_group_defaults: DF.Table[ItemDefault]
		item_group_name: DF.Data
		lft: DF.Int
		old_parent: DF.Link | None
		parent_item_group: DF.Link | None
		rgt: DF.Int
		taxes: DF.Table[ItemTax]
	# end: auto-generated types

	def validate(self):
		if not self.parent_item_group and not nts.flags.in_test:
			if nts.db.exists("Item Group", _("All Item Groups")):
				self.parent_item_group = _("All Item Groups")
		self.validate_item_group_defaults()
		self.check_item_tax()

	def check_item_tax(self):
		"""Check whether Tax Rate is not entered twice for same Tax Type"""
		check_list = []
		for d in self.get("taxes"):
			if d.item_tax_template:
				if (d.item_tax_template, d.tax_category) in check_list:
					nts.throw(
						_("{0} entered twice {1} in Item Taxes").format(
							nts.bold(d.item_tax_template),
							f"for tax category {nts.bold(d.tax_category)}" if d.tax_category else "",
						)
					)
				else:
					check_list.append((d.item_tax_template, d.tax_category))

	def on_update(self):
		NestedSet.on_update(self)
		self.validate_one_root()
		self.delete_child_item_groups_key()

	def on_trash(self):
		NestedSet.on_trash(self, allow_root_deletion=True)
		self.delete_child_item_groups_key()

	def delete_child_item_groups_key(self):
		nts.cache().hdel("child_item_groups", self.name)

	def validate_item_group_defaults(self):
		from prodman.stock.doctype.item.item import validate_item_default_company_links

		validate_item_default_company_links(self.item_group_defaults)


def get_child_item_groups(item_group_name):
	item_group = nts.get_cached_value("Item Group", item_group_name, ["lft", "rgt"], as_dict=1)

	child_item_groups = [
		d.name
		for d in nts.get_all(
			"Item Group", filters={"lft": (">=", item_group.lft), "rgt": ("<=", item_group.rgt)}
		)
	]

	return child_item_groups or {}


def get_item_group_defaults(item, company):
	item = nts.get_cached_doc("Item", item)
	item_group = nts.get_cached_doc("Item Group", item.item_group)

	for d in item_group.item_group_defaults or []:
		if d.company == company:
			row = copy.deepcopy(d.as_dict())
			row.pop("name")
			return row

	return nts._dict()
