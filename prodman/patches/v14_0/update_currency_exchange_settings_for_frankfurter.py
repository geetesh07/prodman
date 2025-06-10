import nts


def execute():
	settings = nts.get_doc("Currency Exchange Settings")
	if settings.service_provider != "frankfurter.app":
		return

	settings.set_parameters_and_result()
	settings.flags.ignore_validate = True
	settings.save()
