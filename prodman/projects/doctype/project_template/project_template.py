# Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.utils import get_link_to_form


class ProjectTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.projects.doctype.project_template_task.project_template_task import (
			ProjectTemplateTask,
		)

		project_type: DF.Link | None
		tasks: DF.Table[ProjectTemplateTask]
	# end: auto-generated types

	def validate(self):
		self.validate_dependencies()

	def validate_dependencies(self):
		for task in self.tasks:
			task_details = nts.get_doc("Task", task.task)
			if task_details.depends_on:
				for dependency_task in task_details.depends_on:
					if not self.check_dependent_task_presence(dependency_task.task):
						task_details_format = get_link_to_form("Task", task_details.name)
						dependency_task_format = get_link_to_form("Task", dependency_task.task)
						nts.throw(
							_("Task {0} depends on Task {1}. Please add Task {1} to the Tasks list.").format(
								nts.bold(task_details_format), nts.bold(dependency_task_format)
							)
						)

	def check_dependent_task_presence(self, task):
		for task_details in self.tasks:
			if task_details.task == task:
				return True
		return False
