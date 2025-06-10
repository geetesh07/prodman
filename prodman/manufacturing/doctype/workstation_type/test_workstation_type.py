# Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase


class TestWorkstationType(ntsTestCase):
	pass


def create_workstation_type(**args):
	args = nts._dict(args)

	if workstation_type := nts.db.exists("Workstation Type", args.workstation_type):
		return nts.get_doc("Workstation Type", workstation_type)
	else:
		doc = nts.new_doc("Workstation Type")
		doc.update(args)
		doc.insert()
		return doc
