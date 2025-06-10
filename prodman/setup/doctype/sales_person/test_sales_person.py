# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

test_dependencies = ["Employee"]

import nts

test_records = nts.get_test_records("Sales Person")

test_ignore = ["Item Group"]
