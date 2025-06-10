import nts


def execute():
	nts.db.sql(
		"""
		UPDATE `tabStock Ledger Entry`
			SET posting_datetime = timestamp(posting_date, posting_time)
	"""
	)
