# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.utils import getdate


def execute():
	nts.reload_doc("setup", "doctype", "transaction_deletion_record")

	if has_deleted_company_transactions():
		child_doctypes = get_child_doctypes_whose_parent_doctypes_were_affected()

		for doctype in child_doctypes:
			docs = nts.get_all(doctype, fields=["name", "parent", "parenttype", "creation"])

			for doc in docs:
				if not nts.db.exists(doc["parenttype"], doc["parent"]):
					nts.db.delete(doctype, {"name": doc["name"]})

				elif check_for_new_doc_with_same_name_as_deleted_parent(doc):
					nts.db.delete(doctype, {"name": doc["name"]})


def has_deleted_company_transactions():
	return nts.get_all("Transaction Deletion Record")


def get_child_doctypes_whose_parent_doctypes_were_affected():
	parent_doctypes = get_affected_doctypes()
	child_doctypes = nts.get_all(
		"DocField", filters={"fieldtype": "Table", "parent": ["in", parent_doctypes]}, pluck="options"
	)

	return child_doctypes


def get_affected_doctypes():
	affected_doctypes = []
	tdr_docs = nts.get_all("Transaction Deletion Record", pluck="name")

	for tdr in tdr_docs:
		tdr_doc = nts.get_doc("Transaction Deletion Record", tdr)

		for doctype in tdr_doc.doctypes:
			if is_not_child_table(doctype.doctype_name):
				affected_doctypes.append(doctype.doctype_name)

	affected_doctypes = remove_duplicate_items(affected_doctypes)
	return affected_doctypes


def is_not_child_table(doctype):
	return not bool(nts.get_value("DocType", doctype, "istable"))


def remove_duplicate_items(affected_doctypes):
	return list(set(affected_doctypes))


def check_for_new_doc_with_same_name_as_deleted_parent(doc):
	"""
	Compares creation times of parent and child docs.
	Since Transaction Deletion Record resets the naming series after deletion,
	it allows the creation of new docs with the same names as the deleted ones.
	"""

	parent_creation_time = nts.db.get_value(doc["parenttype"], doc["parent"], "creation")
	child_creation_time = doc["creation"]

	return getdate(parent_creation_time) > getdate(child_creation_time)
