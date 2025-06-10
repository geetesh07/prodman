import nts


def get_context(context):
	context.no_cache = 1

	timelog = nts.get_doc("Time Log", nts.form_dict.timelog)

	context.doc = timelog
