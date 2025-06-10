import nts


def get_context(context):
	context.no_cache = 1

	task = nts.get_doc("Task", nts.form_dict.task)

	context.comments = nts.get_all(
		"Communication",
		filters={"reference_name": task.name, "comment_type": "comment"},
		fields=["subject", "sender_full_name", "communication_date"],
	)

	context.doc = task
