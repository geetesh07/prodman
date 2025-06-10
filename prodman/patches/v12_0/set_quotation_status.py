import nts


def execute():
	nts.db.sql(
		""" UPDATE `tabQuotation` set status = 'Open'
		where docstatus = 1 and status = 'Submitted' """
	)
