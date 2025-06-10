import nts


def execute():
	install_apps = nts.get_installed_apps()
	if "prodman_datev_uo" in install_apps or "prodman_datev" in install_apps:
		return

	# doctypes
	nts.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	nts.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
