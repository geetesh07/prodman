import json

import nts
from nts import _
from nts.custom.doctype.custom_field.custom_field import create_custom_fields


@nts.whitelist()
def create_custom_fields_for_nts_crm():
	nts.only_for("System Manager")
	custom_fields = {
		"Quotation": [
			{
				"fieldname": "crm_deal",
				"fieldtype": "Data",
				"label": "nts CRM Deal",
				"insert_after": "party_name",
			}
		],
		"Customer": [
			{
				"fieldname": "crm_deal",
				"fieldtype": "Data",
				"label": "nts CRM Deal",
				"insert_after": "prospect_name",
			}
		],
	}
	create_custom_fields(custom_fields, ignore_validate=True)


@nts.whitelist()
def create_prospect_against_crm_deal():
	doc = nts.form_dict
	prospect = nts.get_doc(
		{
			"doctype": "Prospect",
			"company_name": doc.organization or doc.lead_name,
			"no_of_employees": doc.no_of_employees,
			"prospect_owner": doc.deal_owner,
			"company": doc.prodman_company,
			"crm_deal": doc.crm_deal,
			"territory": doc.territory,
			"industry": doc.industry,
			"website": doc.website,
			"annual_revenue": doc.annual_revenue,
		}
	)

	try:
		prospect_name = nts.db.get_value("Prospect", {"company_name": prospect.company_name})
		if not prospect_name:
			prospect.insert()
			prospect_name = prospect.name
	except Exception:
		nts.log_error(
			nts.get_traceback(),
			f"Error while creating prospect against CRM Deal: {nts.form_dict.get('crm_deal_id')}",
		)
		pass

	create_contacts(json.loads(doc.contacts), prospect.company_name, "Prospect", prospect_name)
	create_address("Prospect", prospect_name, doc.address)
	nts.response["message"] = prospect_name


def create_contacts(contacts, organization=None, link_doctype=None, link_docname=None):
	for c in contacts:
		c = nts._dict(c)
		existing_contact = contact_exists(c.email, c.mobile_no)
		if existing_contact:
			contact = nts.get_doc("Contact", existing_contact)
		else:
			contact = nts.get_doc(
				{
					"doctype": "Contact",
					"first_name": c.get("full_name"),
					"gender": c.get("gender"),
					"company_name": organization,
				}
			)

			if c.get("email"):
				contact.append("email_ids", {"email_id": c.get("email"), "is_primary": 1})

			if c.get("mobile_no"):
				contact.append("phone_nos", {"phone": c.get("mobile_no"), "is_primary_mobile_no": 1})

		link_doc(contact, link_doctype, link_docname)

		contact.save(ignore_permissions=True)


def create_address(doctype, docname, address):
	if not address:
		return
	if isinstance(address, str):
		address = json.loads(address)
	try:
		_address = nts.db.exists("Address", address.get("name"))
		if not _address:
			new_address_doc = nts.new_doc("Address")
			for field in [
				"address_title",
				"address_type",
				"address_line1",
				"address_line2",
				"city",
				"county",
				"state",
				"pincode",
				"country",
			]:
				if address.get(field):
					new_address_doc.set(field, address.get(field))

			new_address_doc.append("links", {"link_doctype": doctype, "link_name": docname})
			new_address_doc.insert(ignore_mandatory=True)
			return new_address_doc.name
		else:
			address = nts.get_doc("Address", _address)
			link_doc(address, doctype, docname)
			address.save(ignore_permissions=True)
			return address.name
	except Exception:
		nts.log_error(nts.get_traceback(), f"Error while creating address for {docname}")


def link_doc(doc, link_doctype, link_docname):
	already_linked = any(
		[(link.link_doctype == link_doctype and link.link_name == link_docname) for link in doc.links]
	)
	if not already_linked:
		doc.append(
			"links", {"link_doctype": link_doctype, "link_name": link_docname, "link_title": link_docname}
		)


def contact_exists(email, mobile_no):
	email_exist = nts.db.exists("Contact Email", {"email_id": email})
	mobile_exist = nts.db.exists("Contact Phone", {"phone": mobile_no})

	doctype = "Contact Email" if email_exist else "Contact Phone"
	name = email_exist or mobile_exist

	if name:
		return nts.db.get_value(doctype, name, "parent")

	return False


@nts.whitelist()
def create_customer(customer_data=None):
	if not customer_data:
		customer_data = nts.form_dict

	try:
		customer_name = nts.db.exists("Customer", {"customer_name": customer_data.get("customer_name")})
		if not customer_name:
			customer = nts.get_doc({"doctype": "Customer", **customer_data}).insert(
				ignore_permissions=True
			)
			customer_name = customer.name

		contacts = json.loads(customer_data.get("contacts"))
		create_contacts(contacts, customer_name, "Customer", customer_name)
		create_address("Customer", customer_name, customer_data.get("address"))
		return customer_name
	except Exception:
		nts.log_error(nts.get_traceback(), "Error while creating customer against nts CRM Deal")
		pass
