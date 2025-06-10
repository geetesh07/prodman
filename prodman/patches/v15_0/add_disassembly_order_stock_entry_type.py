import nts


def execute():
	if not nts.db.exists("Stock Entry Type", "Disassemble"):
		nts.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": "Disassemble",
				"purpose": "Disassemble",
				"is_standard": 1,
			}
		).insert(ignore_permissions=True)
