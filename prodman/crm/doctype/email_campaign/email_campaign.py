# Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.core.doctype.communication.email import make
from nts.model.document import Document
from nts.utils import add_days, getdate, today


class EmailCampaign(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		campaign_name: DF.Link
		email_campaign_for: DF.Literal["", "Lead", "Contact", "Email Group"]
		end_date: DF.Date | None
		recipient: DF.DynamicLink
		sender: DF.Link | None
		start_date: DF.Date
		status: DF.Literal["", "Scheduled", "In Progress", "Completed", "Unsubscribed"]
	# end: auto-generated types

	def validate(self):
		self.set_date()
		# checking if email is set for lead. Not checking for contact as email is a mandatory field for contact.
		if self.email_campaign_for == "Lead":
			self.validate_lead()
		self.validate_email_campaign_already_exists()
		self.update_status()

	def set_date(self):
		if getdate(self.start_date) < getdate(today()):
			nts.throw(_("Start Date cannot be before the current date"))
		# set the end date as start date + max(send after days) in campaign schedule
		send_after_days = []
		campaign = nts.get_doc("Campaign", self.campaign_name)
		for entry in campaign.get("campaign_schedules"):
			send_after_days.append(entry.send_after_days)
		try:
			self.end_date = add_days(getdate(self.start_date), max(send_after_days))
		except ValueError:
			nts.throw(
				_("Please set up the Campaign Schedule in the Campaign {0}").format(self.campaign_name)
			)

	def validate_lead(self):
		lead_email_id = nts.db.get_value("Lead", self.recipient, "email_id")
		if not lead_email_id:
			lead_name = nts.db.get_value("Lead", self.recipient, "lead_name")
			nts.throw(_("Please set an email id for the Lead {0}").format(lead_name))

	def validate_email_campaign_already_exists(self):
		email_campaign_exists = nts.db.exists(
			"Email Campaign",
			{
				"campaign_name": self.campaign_name,
				"recipient": self.recipient,
				"status": ("in", ["In Progress", "Scheduled"]),
				"name": ("!=", self.name),
			},
		)
		if email_campaign_exists:
			nts.throw(
				_("The Campaign '{0}' already exists for the {1} '{2}'").format(
					self.campaign_name, self.email_campaign_for, self.recipient
				)
			)

	def update_status(self):
		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)
		today_date = getdate(today())
		if start_date > today_date:
			self.status = "Scheduled"
		elif end_date >= today_date:
			self.status = "In Progress"
		elif end_date < today_date:
			self.status = "Completed"


# called through hooks to send campaign mails to leads
def send_email_to_leads_or_contacts():
	email_campaigns = nts.get_all(
		"Email Campaign", filters={"status": ("not in", ["Unsubscribed", "Completed", "Scheduled"])}
	)
	for camp in email_campaigns:
		email_campaign = nts.get_doc("Email Campaign", camp.name)
		campaign = nts.get_cached_doc("Campaign", email_campaign.campaign_name)
		for entry in campaign.get("campaign_schedules"):
			scheduled_date = add_days(email_campaign.get("start_date"), entry.get("send_after_days"))
			if scheduled_date == getdate(today()):
				send_mail(entry, email_campaign)


def send_mail(entry, email_campaign):
	recipient_list = []
	if email_campaign.email_campaign_for == "Email Group":
		for member in nts.db.get_list(
			"Email Group Member", filters={"email_group": email_campaign.get("recipient")}, fields=["email"]
		):
			recipient_list.append(member["email"])
	else:
		recipient_list.append(
			nts.db.get_value(
				email_campaign.email_campaign_for, email_campaign.get("recipient"), "email_id"
			)
		)

	email_template = nts.get_doc("Email Template", entry.get("email_template"))
	sender = nts.db.get_value("User", email_campaign.get("sender"), "email")
	context = {"doc": nts.get_doc(email_campaign.email_campaign_for, email_campaign.recipient)}
	# send mail and link communication to document
	comm = make(
		doctype="Email Campaign",
		name=email_campaign.name,
		subject=nts.render_template(email_template.get("subject"), context),
		content=nts.render_template(email_template.response_, context),
		sender=sender,
		recipients=recipient_list,
		communication_medium="Email",
		sent_or_received="Sent",
		send_email=True,
		email_template=email_template.name,
	)
	return comm


# called from hooks on doc_event Email Unsubscribe
def unsubscribe_recipient(unsubscribe, method):
	if unsubscribe.reference_doctype == "Email Campaign":
		nts.db.set_value("Email Campaign", unsubscribe.reference_name, "status", "Unsubscribed")


# called through hooks to update email campaign status daily
def set_email_campaign_status():
	email_campaigns = nts.get_all("Email Campaign", filters={"status": ("!=", "Unsubscribed")})
	for entry in email_campaigns:
		email_campaign = nts.get_doc("Email Campaign", entry.name)
		email_campaign.update_status()
