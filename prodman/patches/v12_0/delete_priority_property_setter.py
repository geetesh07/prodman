import nts


def execute():
	nts.db.sql(
		"""
		DELETE FROM `tabProperty Setter`
		WHERE `tabProperty Setter`.doc_type='Issue'
			AND `tabProperty Setter`.field_name='priority'
			AND `tabProperty Setter`.property='options'
	"""
	)
