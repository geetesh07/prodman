# Copyright (c) 2020, nts Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if nts.db.has_column("Member", "email"):
		# Get all members
		for member in nts.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not nts.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = nts.db.get_value("Member", member, "email")

				# Set the value for it
				nts.db.set_value("Member", member, "email_id", email)

	if nts.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
