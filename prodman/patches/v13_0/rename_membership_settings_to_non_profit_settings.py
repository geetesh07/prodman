import nts
from nts.model.utils.rename_field import rename_field


def execute():
	if nts.db.table_exists("Membership Settings"):
		nts.rename_doc("DocType", "Membership Settings", "Non Profit Settings")
		nts.reload_doctype("Non Profit Settings", force=True)

	if nts.db.table_exists("Non Profit Settings"):
		rename_fields_map = {
			"enable_invoicing": "allow_invoicing",
			"create_for_web_forms": "automate_membership_invoicing",
			"make_payment_entry": "automate_membership_payment_entries",
			"enable_razorpay": "enable_razorpay_for_memberships",
			"debit_account": "membership_debit_account",
			"payment_account": "membership_payment_account",
			"webhook_secret": "membership_webhook_secret",
		}

		for old_name, new_name in rename_fields_map.items():
			rename_field("Non Profit Settings", old_name, new_name)
