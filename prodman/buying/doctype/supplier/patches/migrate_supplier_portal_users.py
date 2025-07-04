import os

import nts

in_ci = os.environ.get("CI")


def execute():
	try:
		contacts = get_portal_user_contacts()
		add_portal_users(contacts)
	except Exception:
		nts.db.rollback()
		nts.log_error("Failed to migrate portal users")

		if in_ci:  # TODO: better way to handle this.
			raise


def get_portal_user_contacts():
	contact = nts.qb.DocType("Contact")
	dynamic_link = nts.qb.DocType("Dynamic Link")

	return (
		nts.qb.from_(contact)
		.inner_join(dynamic_link)
		.on(contact.name == dynamic_link.parent)
		.select(
			(dynamic_link.link_doctype).as_("doctype"),
			(dynamic_link.link_name).as_("parent"),
			(contact.email_id).as_("portal_user"),
		)
		.where(
			(dynamic_link.parenttype == "Contact")
			& (dynamic_link.link_doctype.isin(["Supplier", "Customer"]))
		)
	).run(as_dict=True)


def add_portal_users(contacts):
	for contact in contacts:
		user = nts.db.get_value("User", {"email": contact.portal_user}, "name")
		if not user:
			continue

		roles = nts.get_roles(user)
		required_role = contact.doctype
		if required_role not in roles:
			continue

		portal_user_doc = nts.new_doc("Portal User")
		portal_user_doc.parenttype = contact.doctype
		portal_user_doc.parentfield = "portal_users"
		portal_user_doc.parent = contact.parent
		portal_user_doc.user = user
		portal_user_doc.insert()
