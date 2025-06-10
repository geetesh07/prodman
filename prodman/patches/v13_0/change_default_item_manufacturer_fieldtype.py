import nts


def execute():
	# Erase all default item manufacturers that dont exist.
	item = nts.qb.DocType("Item")
	manufacturer = nts.qb.DocType("Manufacturer")

	(
		nts.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
