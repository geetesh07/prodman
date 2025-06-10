import nts


def execute():
	nts.reload_doc("core", "doctype", "scheduled_job_type")
	if nts.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		nts.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
