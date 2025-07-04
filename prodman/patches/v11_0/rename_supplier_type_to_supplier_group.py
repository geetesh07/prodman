import nts
from nts import _
from nts.model.utils.rename_field import rename_field
from nts.utils.nestedset import rebuild_tree


def execute():
	if nts.db.table_exists("Supplier Group"):
		nts.reload_doc("setup", "doctype", "supplier_group")
	elif nts.db.table_exists("Supplier Type"):
		nts.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		nts.reload_doc("setup", "doctype", "supplier_group")
		nts.reload_doc("accounts", "doctype", "pricing_rule")
		nts.reload_doc("accounts", "doctype", "tax_rule")
		nts.reload_doc("buying", "doctype", "buying_settings")
		nts.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	nts.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{}'
		where is_group = 0""".format(_("All Supplier Groups"))
	)

	if not nts.db.exists("Supplier Group", _("All Supplier Groups")):
		nts.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group", "parent_supplier_group")
