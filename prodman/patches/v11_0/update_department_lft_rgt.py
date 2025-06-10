import nts
from nts import _
from nts.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	nts.reload_doc("setup", "doctype", "department")
	if not nts.db.exists("Department", _("All Departments")):
		nts.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	nts.db.sql(
		"""update `tabDepartment` set parent_department = '{}'
		where is_group = 0""".format(_("All Departments"))
	)

	rebuild_tree("Department", "parent_department")
