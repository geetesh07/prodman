# Copyright (c) 2021, Wahni Green Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts 
from nts  import _
from nts .model.document import Document
from nts .utils.background_jobs import is_job_enqueued

from prodman.accounts.doctype.account.account import merge_account


class LedgerMerge(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.ledger_merge_accounts.ledger_merge_accounts import (
			LedgerMergeAccounts,
		)

		account: DF.Link
		account_name: DF.Data
		company: DF.Link
		is_group: DF.Check
		merge_accounts: DF.Table[LedgerMergeAccounts]
		root_type: DF.Literal["", "Asset", "Liability", "Income", "Expense", "Equity"]
		status: DF.Literal["Pending", "Success", "Partial Success", "Error"]
	# end: auto-generated types

	def start_merge(self):
		from nts .utils.background_jobs import enqueue
		from nts .utils.scheduler import is_scheduler_inactive

		if is_scheduler_inactive() and not nts .flags.in_test:
			nts .throw(_("Scheduler is inactive. Cannot merge accounts."), title=_("Scheduler Inactive"))

		job_id = f"ledger_merge::{self.name}"
		if not is_job_enqueued(job_id):
			enqueue(
				start_merge,
				queue="default",
				timeout=6000,
				event="ledger_merge",
				job_id=job_id,
				docname=self.name,
				now=nts .conf.developer_mode or nts .flags.in_test,
			)
			return True

		return False


@nts .whitelist()
def form_start_merge(docname):
	return nts .get_doc("Ledger Merge", docname).start_merge()


def start_merge(docname):
	ledger_merge = nts .get_doc("Ledger Merge", docname)
	successful_merges = 0
	total = len(ledger_merge.merge_accounts)
	for row in ledger_merge.merge_accounts:
		if not row.merged:
			try:
				merge_account(
					row.account,
					ledger_merge.account,
				)
				row.db_set("merged", 1)
				nts .db.commit()
				successful_merges += 1
				nts .publish_realtime(
					"ledger_merge_progress",
					{"ledger_merge": ledger_merge.name, "current": successful_merges, "total": total},
				)
			except Exception:
				nts .db.rollback()
				ledger_merge.log_error("Ledger merge failed")
			finally:
				if successful_merges == total:
					ledger_merge.db_set("status", "Success")
				elif successful_merges > 0:
					ledger_merge.db_set("status", "Partial Success")
				else:
					ledger_merge.db_set("status", "Error")

	nts .publish_realtime("ledger_merge_refresh", {"ledger_merge": ledger_merge.name})
