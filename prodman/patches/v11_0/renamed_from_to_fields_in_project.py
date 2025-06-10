# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("projects", "doctype", "project")

	if nts.db.has_column("Project", "from"):
		rename_field("Project", "from", "from_time")
		rename_field("Project", "to", "to_time")
