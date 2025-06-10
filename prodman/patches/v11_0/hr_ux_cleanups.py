import nts


def execute():
	nts.reload_doctype("Employee")
	nts.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	nts.reload_doctype("Holiday List")
	for holiday_list in nts.get_all("Holiday List"):
		holiday_list = nts.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
