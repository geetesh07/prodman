import nts


def execute():
	"""Set the payment gateway account as Email for all the existing payment channel."""
	doc_meta = nts.get_meta("Payment Gateway Account")
	if doc_meta.get_field("payment_channel"):
		return

	nts.reload_doc("Accounts", "doctype", "Payment Gateway Account")
	set_payment_channel_as_email()


def set_payment_channel_as_email():
	nts.db.sql(
		"""
		UPDATE `tabPayment Gateway Account`
		SET `payment_channel` = "Email"
	"""
	)
