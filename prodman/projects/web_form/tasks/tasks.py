import nts


def get_context(context):
	if nts.form_dict.project:
		context.parents = [
			{"title": nts.form_dict.project, "route": "/projects?project=" + nts.form_dict.project}
		]
		context.success_url = "/projects?project=" + nts.form_dict.project

	elif context.doc and context.doc.get("project"):
		context.parents = [
			{"title": context.doc.project, "route": "/projects?project=" + context.doc.project}
		]
		context.success_url = "/projects?project=" + context.doc.project
