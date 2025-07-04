# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts import _
from nts.utils import flt
from nts.utils.nestedset import NestedSet, get_root_of


class Territory(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.setup.doctype.target_detail.target_detail import TargetDetail

		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_territory: DF.Link | None
		rgt: DF.Int
		targets: DF.Table[TargetDetail]
		territory_manager: DF.Link | None
		territory_name: DF.Data
	# end: auto-generated types

	nsm_parent_field = "parent_territory"

	def validate(self):
		if not self.parent_territory:
			self.parent_territory = get_root_of("Territory")

		for d in self.get("targets") or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				nts.throw(_("Either target qty or target amount is mandatory"))

	def on_update(self):
		super().on_update()
		self.validate_one_root()


def on_doctype_update():
	nts.db.add_index("Territory", ["lft", "rgt"])
