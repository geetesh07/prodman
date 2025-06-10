# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts

test_records = nts.get_test_records("Operation")


class TestOperation(unittest.TestCase):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = nts._dict(args)

	if not nts.db.exists("Operation", args.operation):
		doc = nts.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return nts.get_doc("Operation", args.operation)
