# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.utils.nestedset import NestedSet, get_root_of

from prodman.utilities.transaction_base import delete_events


class Department(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		company: DF.Link
		department_name: DF.Data
		disabled: DF.Check
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Data | None
		parent_department: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	nsm_parent_field = "parent_department"

	def autoname(self):
		root = get_root_of("Department")
		if root and self.department_name != root:
			self.name = get_abbreviated_name(self.department_name, self.company)
		else:
			self.name = self.department_name

	def validate(self):
		if not self.parent_department:
			root = get_root_of("Department")
			if root:
				self.parent_department = root

	def before_rename(self, old, new, merge=False):
		# renaming consistency with abbreviation
		if nts.get_cached_value("Company", self.company, "abbr") not in new:
			new = get_abbreviated_name(new, self.company)

		return new

	def on_update(self):
		if not (nts.local.flags.ignore_update_nsm or nts.flags.in_setup_wizard):
			super().on_update()

	def on_trash(self):
		super().on_trash()
		delete_events(self.doctype, self.name)


def on_doctype_update():
	nts.db.add_index("Department", ["lft", "rgt"])


def get_abbreviated_name(name, company):
	abbr = nts.get_cached_value("Company", company, "abbr")
	new_name = f"{name} - {abbr}"
	return new_name


@nts.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	fields = ["name as value", "is_group as expandable"]
	filters = {}

	if company == parent:
		filters["name"] = get_root_of("Department")
	elif company:
		filters["parent_department"] = parent
		filters["company"] = company
	else:
		filters["parent_department"] = parent

	return nts.get_all("Department", fields=fields, filters=filters, order_by="name")


@nts.whitelist()
def add_node():
	from nts.desk.treeview import make_tree_args

	args = nts.form_dict
	args = make_tree_args(**args)

	if args.parent_department == args.company:
		args.parent_department = None

	nts.get_doc(args).insert()
