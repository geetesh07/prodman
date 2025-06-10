# Copyright (c) 2018, nts  Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts 
from nts  import _
from nts .model.document import Document
from nts .utils import flt, today


class LoyaltyProgram(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts .types import DF

		from prodman.accounts.doctype.loyalty_program_collection.loyalty_program_collection import (
			LoyaltyProgramCollection,
		)

		auto_opt_in: DF.Check
		collection_rules: DF.Table[LoyaltyProgramCollection]
		company: DF.Link | None
		conversion_factor: DF.Float
		cost_center: DF.Link | None
		customer_group: DF.Link | None
		customer_territory: DF.Link | None
		expense_account: DF.Link | None
		expiry_duration: DF.Int
		from_date: DF.Date
		loyalty_program_name: DF.Data
		loyalty_program_type: DF.Literal["Single Tier Program", "Multiple Tier Program"]
		to_date: DF.Date | None
	# end: auto-generated types

	pass


def get_loyalty_details(
	customer, loyalty_program, expiry_date=None, company=None, include_expired_entry=False
):
	if not expiry_date:
		expiry_date = today()

	condition = ""
	if company:
		condition = " and company=%s " % nts .db.escape(company)
	if not include_expired_entry:
		condition += " and expiry_date>='%s' " % expiry_date

	loyalty_point_details = nts .db.sql(
		f"""select sum(loyalty_points) as loyalty_points,
		sum(purchase_amount) as total_spent from `tabLoyalty Point Entry`
		where customer=%s and loyalty_program=%s and posting_date <= %s
		{condition}
		group by customer""",
		(customer, loyalty_program, expiry_date),
		as_dict=1,
	)

	if loyalty_point_details:
		return loyalty_point_details[0]
	else:
		return {"loyalty_points": 0, "total_spent": 0}


@nts .whitelist()
def get_loyalty_program_details_with_points(
	customer,
	loyalty_program=None,
	expiry_date=None,
	company=None,
	silent=False,
	include_expired_entry=False,
	current_transaction_amount=0,
):
	lp_details = get_loyalty_program_details(customer, loyalty_program, company=company, silent=silent)
	loyalty_program = nts .get_doc("Loyalty Program", loyalty_program)
	lp_details.update(
		get_loyalty_details(customer, loyalty_program.name, expiry_date, company, include_expired_entry)
	)

	tier_spent_level = sorted(
		[d.as_dict() for d in loyalty_program.collection_rules],
		key=lambda rule: rule.min_spent,
		reverse=True,
	)
	for i, d in enumerate(tier_spent_level):
		if i == 0 or (lp_details.total_spent + current_transaction_amount) <= d.min_spent:
			lp_details.tier_name = d.tier_name
			lp_details.collection_factor = d.collection_factor
		else:
			break

	return lp_details


@nts .whitelist()
def get_loyalty_program_details(
	customer,
	loyalty_program=None,
	expiry_date=None,
	company=None,
	silent=False,
	include_expired_entry=False,
):
	lp_details = nts ._dict()

	if not loyalty_program:
		loyalty_program = nts .db.get_value("Customer", customer, "loyalty_program")

		if not loyalty_program and not silent:
			nts .throw(_("Customer isn't enrolled in any Loyalty Program"))
		elif silent and not loyalty_program:
			return nts ._dict({"loyalty_programs": None})

	if not company:
		company = nts .db.get_default("company") or nts .get_all("Company")[0].name

	loyalty_program = nts .get_doc("Loyalty Program", loyalty_program)
	lp_details.update({"loyalty_program": loyalty_program.name})
	lp_details.update(loyalty_program.as_dict())
	return lp_details


@nts .whitelist()
def get_redeemption_factor(loyalty_program=None, customer=None):
	customer_loyalty_program = None
	if not loyalty_program:
		customer_loyalty_program = nts .db.get_value("Customer", customer, "loyalty_program")
		loyalty_program = customer_loyalty_program
	if loyalty_program:
		return nts .db.get_value("Loyalty Program", loyalty_program, "conversion_factor")
	else:
		nts .throw(_("Customer isn't enrolled in any Loyalty Program"))


def validate_loyalty_points(ref_doc, points_to_redeem):
	loyalty_program = None
	posting_date = None

	if ref_doc.doctype == "Sales Invoice":
		posting_date = ref_doc.posting_date
	else:
		posting_date = today()

	if hasattr(ref_doc, "loyalty_program") and ref_doc.loyalty_program:
		loyalty_program = ref_doc.loyalty_program
	else:
		loyalty_program = nts .db.get_value("Customer", ref_doc.customer, ["loyalty_program"])

	if (
		loyalty_program
		and nts .db.get_value("Loyalty Program", loyalty_program, ["company"]) != ref_doc.company
	):
		nts .throw(_("The Loyalty Program isn't valid for the selected company"))

	if loyalty_program and points_to_redeem:
		loyalty_program_details = get_loyalty_program_details_with_points(
			ref_doc.customer, loyalty_program, posting_date, ref_doc.company
		)

		if points_to_redeem > loyalty_program_details.loyalty_points:
			nts .throw(_("You don't have enough Loyalty Points to redeem"))

		loyalty_amount = flt(points_to_redeem * loyalty_program_details.conversion_factor)

		total_amount = ref_doc.grand_total if ref_doc.is_rounded_total_disabled() else ref_doc.rounded_total
		if loyalty_amount > total_amount:
			nts .throw(_("You can't redeem Loyalty Points having more value than the Total Amount."))

		if not ref_doc.loyalty_amount and ref_doc.loyalty_amount != loyalty_amount:
			ref_doc.loyalty_amount = loyalty_amount

		if ref_doc.doctype == "Sales Invoice":
			ref_doc.loyalty_program = loyalty_program
			if not ref_doc.loyalty_redemption_account:
				ref_doc.loyalty_redemption_account = loyalty_program_details.expense_account

			if not ref_doc.loyalty_redemption_cost_center:
				ref_doc.loyalty_redemption_cost_center = loyalty_program_details.cost_center

		elif ref_doc.doctype == "Sales Order":
			return loyalty_amount
