# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import nts
from nts.model.document import Document
from nts.model.rename_doc import bulk_rename


class RenameTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		file_to_rename: DF.Attach | None
		select_doctype: DF.Literal
	# end: auto-generated types

	pass


@nts.whitelist()
def get_doctypes():
	return nts.db.sql_list(
		"""select name from tabDocType
		where allow_rename=1 and module!='Core' order by name"""
	)


@nts.whitelist()
def upload(select_doctype=None, rows=None):
	from nts.utils.csvutils import read_csv_content_from_attached_file

	if not select_doctype:
		select_doctype = nts.form_dict.select_doctype

	if not nts.has_permission(select_doctype, "write"):
		raise nts.PermissionError

	rows = read_csv_content_from_attached_file(nts.get_doc("Rename Tool", "Rename Tool"))

	# bulk rename allows only 500 rows at a time, so we created one job per 500 rows
	for i in range(0, len(rows), 500):
		nts.enqueue(
			method=bulk_rename,
			queue="long",
			doctype=select_doctype,
			rows=rows[i : i + 500],
		)
