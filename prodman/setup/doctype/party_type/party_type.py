# Copyright (c) 2015, nts Technologies and contributors
# For license information, please see license.txt


import nts
from nts.model.document import Document


class PartyType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		account_type: DF.Literal["Payable", "Receivable"]
		party_type: DF.Link
	# end: auto-generated types

	pass


@nts.whitelist()
@nts.validate_and_sanitize_search_inputs
def get_party_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ""
	if filters and filters.get("account"):
		account_type = nts.db.get_value("Account", filters.get("account"), "account_type")
		cond = "and account_type = '%s'" % account_type

	return nts.db.sql(
		f"""select name from `tabParty Type`
			where `{searchfield}` LIKE %(txt)s {cond}
			order by name limit %(page_len)s offset %(start)s""",
		{"txt": "%" + txt + "%", "start": start, "page_len": page_len},
	)
