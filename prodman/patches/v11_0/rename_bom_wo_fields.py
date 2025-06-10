# Copyright (c) 2018, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts.model.utils.rename_field import rename_field


def execute():
	# updating column value to handle field change from Data to Currency
	changed_field = "base_scrap_material_cost"
	nts.db.sql(f"update `tabBOM` set {changed_field} = '0' where trim(coalesce({changed_field}, ''))= ''")

	for doctype in ["BOM Explosion Item", "BOM Item", "Work Order Item", "Item"]:
		if nts.db.has_column(doctype, "allow_transfer_for_manufacture"):
			if doctype != "Item":
				nts.reload_doc("manufacturing", "doctype", nts.scrub(doctype))
			else:
				nts.reload_doc("stock", "doctype", nts.scrub(doctype))

			rename_field(doctype, "allow_transfer_for_manufacture", "include_item_in_manufacturing")

	for doctype in ["BOM", "Work Order"]:
		nts.reload_doc("manufacturing", "doctype", nts.scrub(doctype))

		if nts.db.has_column(doctype, "transfer_material_against_job_card"):
			nts.db.sql(
				""" UPDATE `tab%s`
                SET transfer_material_against = CASE WHEN
                    transfer_material_against_job_card = 1 then 'Job Card' Else 'Work Order' END
                WHERE docstatus < 2"""
				% (doctype)
			)
		else:
			nts.db.sql(
				""" UPDATE `tab%s`
                SET transfer_material_against = 'Work Order'
                WHERE docstatus < 2"""
				% (doctype)
			)
