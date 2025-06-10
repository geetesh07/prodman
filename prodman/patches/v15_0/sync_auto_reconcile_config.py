import nts

from prodman.accounts.utils import sync_auto_reconcile_config


def execute():
	"""
	Set default Cron Interval and Queue size
	"""
	nts.db.set_single_value("Accounts Settings", "auto_reconciliation_job_trigger", 15)
	nts.db.set_single_value("Accounts Settings", "reconciliation_queue_size", 5)

	# Create Scheduler Event record if it doesn't exist
	if nts.reload_doc("core", "doctype", "scheduler_event"):
		method = "prodman.accounts.doctype.process_payment_reconciliation.process_payment_reconciliation.trigger_reconciliation_for_queued_docs"
		if not nts.db.get_all(
			"Scheduler Event", {"scheduled_against": "Process Payment Reconciliation", "method": method}
		):
			nts.get_doc(
				{
					"doctype": "Scheduler Event",
					"scheduled_against": "Process Payment Reconciliation",
					"method": method,
				}
			).save()

		sync_auto_reconcile_config(15)
