import nts


def execute():
	nts.reload_doctype("Maintenance Visit")
	nts.reload_doctype("Maintenance Visit Purpose")

	# Updates the Maintenance Schedule link to fetch serial nos
	from nts.query_builder.functions import Coalesce

	mvp = nts.qb.DocType("Maintenance Visit Purpose")
	mv = nts.qb.DocType("Maintenance Visit")

	nts.qb.update(mv).join(mvp).on(mvp.parent == mv.name).set(
		mv.maintenance_schedule, Coalesce(mvp.prevdoc_docname, "")
	).where((mv.maintenance_type == "Scheduled") & (mvp.prevdoc_docname.notnull()) & (mv.docstatus < 2)).run(
		as_dict=1
	)
