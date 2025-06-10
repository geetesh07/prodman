import nts


def execute():
	if nts.db.get_value("Journal Entry Account", {"reference_due_date": ""}):
		nts.db.sql(
			"""
			UPDATE `tabJournal Entry Account`
			SET reference_due_date = NULL
			WHERE reference_due_date = ''
		"""
		)
