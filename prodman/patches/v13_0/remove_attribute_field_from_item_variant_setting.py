import nts


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	nts.reload_doc("stock", "doctype", "Item Variant Settings")

	nts.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
