import nts


def execute():
	nts.reload_doc("stock", "doctype", "item_variant_attribute")
	nts.db.sql(
		"""
		UPDATE `tabItem Variant Attribute` t1
		INNER JOIN `tabItem` t2 ON t2.name = t1.parent
		SET t1.variant_of = t2.variant_of
	"""
	)
