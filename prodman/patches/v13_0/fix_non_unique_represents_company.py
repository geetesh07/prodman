import nts


def execute():
	nts.db.sql(
		"""
		update tabCustomer
		set represents_company = NULL
		where represents_company = ''
	"""
	)
