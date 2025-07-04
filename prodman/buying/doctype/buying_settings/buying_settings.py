# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import nts
from nts.model.document import Document


class BuyingSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		allow_multiple_items: DF.Check
		allow_zero_qty_in_purchase_order: DF.Check
		allow_zero_qty_in_request_for_quotation: DF.Check
		allow_zero_qty_in_supplier_quotation: DF.Check
		auto_create_purchase_receipt: DF.Check
		auto_create_subcontracting_order: DF.Check
		backflush_raw_materials_of_subcontract_based_on: DF.Literal[
			"BOM", "Material Transferred for Subcontract"
		]
		bill_for_rejected_quantity_in_purchase_invoice: DF.Check
		blanket_order_allowance: DF.Float
		buying_price_list: DF.Link | None
		disable_last_purchase_rate: DF.Check
		maintain_same_rate: DF.Check
		maintain_same_rate_action: DF.Literal["Stop", "Warn"]
		over_transfer_allowance: DF.Float
		po_required: DF.Literal["No", "Yes"]
		pr_required: DF.Literal["No", "Yes"]
		project_update_frequency: DF.Literal["Each Transaction", "Manual"]
		role_to_override_stop_action: DF.Link | None
		set_landed_cost_based_on_purchase_invoice_rate: DF.Check
		set_valuation_rate_for_rejected_materials: DF.Check
		show_pay_button: DF.Check
		supp_master_name: DF.Literal["Supplier Name", "Naming Series", "Auto Name"]
		supplier_group: DF.Link | None
		use_transaction_date_exchange_rate: DF.Check
	# end: auto-generated types

	def validate(self):
		for key in ["supplier_group", "supp_master_name", "maintain_same_rate", "buying_price_list"]:
			nts.db.set_default(key, self.get(key, ""))

		from prodman.utilities.naming import set_by_naming_series

		set_by_naming_series(
			"Supplier",
			"supplier_name",
			self.get("supp_master_name") == "Naming Series",
			hide_name_field=False,
		)

		if not self.bill_for_rejected_quantity_in_purchase_invoice:
			self.set_valuation_rate_for_rejected_materials = 0

	def before_save(self):
		self.check_maintain_same_rate()

	def check_maintain_same_rate(self):
		if self.maintain_same_rate:
			self.set_landed_cost_based_on_purchase_invoice_rate = 0
