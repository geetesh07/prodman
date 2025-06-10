# Copyright (c) 2023, nts Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import nts
from pypika.terms import ExistsCriterion


def execute():
	pl = nts.qb.DocType("Pick List")
	se = nts.qb.DocType("Stock Entry")
	dn = nts.qb.DocType("Delivery Note")

	(
		nts.qb.update(pl).set(
			pl.status,
			(
				nts.qb.terms.Case()
				.when(pl.docstatus == 0, "Draft")
				.when(pl.docstatus == 2, "Cancelled")
				.else_("Completed")
			),
		)
	).run()

	(
		nts.qb.update(pl)
		.set(pl.status, "Open")
		.where(
			(
				ExistsCriterion(
					nts.qb.from_(se).select(se.name).where((se.docstatus == 1) & (se.pick_list == pl.name))
				)
				| ExistsCriterion(
					nts.qb.from_(dn).select(dn.name).where((dn.docstatus == 1) & (dn.pick_list == pl.name))
				)
			).negate()
			& (pl.docstatus == 1)
		)
	).run()
