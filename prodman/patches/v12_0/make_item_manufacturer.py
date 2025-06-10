# Copyright (c) 2017, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	nts.reload_doc("stock", "doctype", "item_manufacturer")

	item_manufacturer = []
	for d in nts.db.sql(
		""" SELECT name, manufacturer, manufacturer_part_no, creation, owner
		FROM `tabItem` WHERE manufacturer is not null and manufacturer != ''""",
		as_dict=1,
	):
		item_manufacturer.append(
			(
				nts.generate_hash("", 10),
				d.name,
				d.manufacturer,
				d.manufacturer_part_no,
				d.creation,
				d.owner,
			)
		)

	if item_manufacturer:
		nts.db.sql(
			"""
			INSERT INTO `tabItem Manufacturer`
			(`name`, `item_code`, `manufacturer`, `manufacturer_part_no`, `creation`, `owner`)
			VALUES {}""".format(", ".join(["%s"] * len(item_manufacturer))),
			tuple(item_manufacturer),
		)
