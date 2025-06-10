import nts


def execute():
	nts.reload_doctype("System Settings")
	settings = nts.get_doc("System Settings")
	settings.db_set("app_name", "prodman", commit=True)
