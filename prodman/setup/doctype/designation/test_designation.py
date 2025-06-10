# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import nts

# test_records = nts.get_test_records('Designation')


def create_designation(**args):
	args = nts._dict(args)
	if nts.db.exists("Designation", args.designation_name or "_Test designation"):
		return nts.get_doc("Designation", args.designation_name or "_Test designation")

	designation = nts.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
