import nts


def execute():
	active_sla_documents = [
		sla.document_type for sla in nts.get_all("Service Level Agreement", fields=["document_type"])
	]

	for doctype in active_sla_documents:
		doctype = nts.qb.DocType(doctype)
		try:
			nts.qb.update(doctype).set(doctype.agreement_status, "First Response Due").where(
				doctype.first_responded_on.isnull()
			).run()

			nts.qb.update(doctype).set(doctype.agreement_status, "Resolution Due").where(
				doctype.agreement_status == "Ongoing"
			).run()

		except Exception:
			nts.log_error("Failed to Patch SLA Status")
