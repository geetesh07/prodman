import nts


def execute():
	if "Education" in nts.get_active_domains() and not nts.db.exists("Role", "Guardian"):
		doc = nts.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
