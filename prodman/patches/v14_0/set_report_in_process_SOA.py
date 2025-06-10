# Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import nts


def execute():
	process_soa = nts.qb.DocType("Process Statement Of Accounts")
	q = nts.qb.update(process_soa).set(process_soa.report, "General Ledger")
	q.run()
