import nts
from nts.utils.nestedset import rebuild_tree


def execute():
	nts.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company", "parent_company")
