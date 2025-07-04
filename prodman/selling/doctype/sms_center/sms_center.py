# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts import _, msgprint
from nts.core.doctype.sms_settings.sms_settings import send_sms
from nts.model.document import Document
from nts.utils import cstr


class SMSCenter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		branch: DF.Link | None
		customer: DF.Link | None
		department: DF.Link | None
		message: DF.Text
		receiver_list: DF.Code | None
		sales_partner: DF.Link | None
		send_to: DF.Literal[
			"",
			"All Contact",
			"All Customer Contact",
			"All Supplier Contact",
			"All Sales Partner Contact",
			"All Lead (Open)",
			"All Employee (Active)",
			"All Sales Person",
		]
		supplier: DF.Link | None
		total_characters: DF.Int
		total_messages: DF.Int
	# end: auto-generated types

	@nts.whitelist()
	def create_receiver_list(self):
		rec, where_clause = "", ""
		if self.send_to == "All Customer Contact":
			where_clause = " and dl.link_doctype = 'Customer'"
			if self.customer:
				where_clause += (
					" and dl.link_name = '%s'" % self.customer.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to == "All Supplier Contact":
			where_clause = " and dl.link_doctype = 'Supplier'"
			if self.supplier:
				where_clause += (
					" and dl.link_name = '%s'" % self.supplier.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to == "All Sales Partner Contact":
			where_clause = " and dl.link_doctype = 'Sales Partner'"
			if self.sales_partner:
				where_clause += (
					"and dl.link_name = '%s'" % self.sales_partner.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to in [
			"All Contact",
			"All Customer Contact",
			"All Supplier Contact",
			"All Sales Partner Contact",
		]:
			rec = nts.db.sql(
				"""select CONCAT(ifnull(c.first_name,''), ' ', ifnull(c.last_name,'')),
				c.mobile_no from `tabContact` c, `tabDynamic Link` dl  where ifnull(c.mobile_no,'')!='' and
				c.docstatus != 2 and dl.parent = c.name%s"""
				% where_clause
			)

		elif self.send_to == "All Lead (Open)":
			rec = nts.db.sql(
				"""select lead_name, mobile_no from `tabLead` where
				ifnull(mobile_no,'')!='' and docstatus != 2 and status='Open'"""
			)

		elif self.send_to == "All Employee (Active)":
			where_clause = (
				self.department and " and department = '%s'" % self.department.replace("'", "'") or ""
			)
			where_clause += self.branch and " and branch = '%s'" % self.branch.replace("'", "'") or ""

			rec = nts.db.sql(
				"""select employee_name, cell_number from
				`tabEmployee` where status = 'Active' and docstatus < 2 and
				ifnull(cell_number,'')!='' %s"""
				% where_clause
			)

		elif self.send_to == "All Sales Person":
			rec = nts.db.sql(
				"""select sales_person_name,
				tabEmployee.cell_number from `tabSales Person` left join tabEmployee
				on `tabSales Person`.employee = tabEmployee.name
				where ifnull(tabEmployee.cell_number,'')!=''"""
			)

		rec_list = ""
		for d in rec:
			rec_list += d[0] + " - " + d[1] + "\n"
		self.receiver_list = rec_list

	def get_receiver_nos(self):
		receiver_nos = []
		if self.receiver_list:
			for d in self.receiver_list.split("\n"):
				receiver_no = d
				if "-" in d:
					receiver_no = receiver_no.split("-")[1]
				if receiver_no.strip():
					receiver_nos.append(cstr(receiver_no).strip())
		else:
			msgprint(_("Receiver List is empty. Please create Receiver List"))

		return receiver_nos

	@nts.whitelist()
	def send_sms(self):
		receiver_list = []
		if not self.message:
			msgprint(_("Please enter message before sending"))
		else:
			receiver_list = self.get_receiver_nos()
		if receiver_list:
			send_sms(receiver_list, cstr(self.message))
