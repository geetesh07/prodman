# Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts.model.document import Document


class Incoterm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		code: DF.Data
		description: DF.LongText | None
		title: DF.Data
	# end: auto-generated types

	pass


def create_incoterms():
	"""Create Incoterm records from incoterms.csv."""
	import os
	from csv import DictReader

	with open(os.path.join(os.path.dirname(__file__), "incoterms.csv")) as f:
		for incoterm in DictReader(f):
			if nts.db.exists("Incoterm", incoterm["code"]):
				continue

			doc = nts.new_doc("Incoterm")
			doc.update(incoterm)
			doc.save()
