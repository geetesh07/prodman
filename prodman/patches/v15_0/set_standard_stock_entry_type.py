import nts


def execute():
	for stock_entry_type in [
		"Material Issue",
		"Material Receipt",
		"Material Transfer",
		"Material Transfer for Manufacture",
		"Material Consumption for Manufacture",
		"Manufacture",
		"Repack",
		"Send to Subcontractor",
		"Disassemble",
	]:
		if nts.db.exists("Stock Entry Type", stock_entry_type):
			nts.db.set_value("Stock Entry Type", stock_entry_type, "is_standard", 1)
