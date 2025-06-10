import nts


def execute():
	if nts.get_all("Company", filters={"country": "India"}, limit=1):
		nts.db.set_single_value("Stock Settings", "allow_existing_serial_no", 1)
