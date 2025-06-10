import nts
from nts.query_builder import DocType


def execute():
	POSInvoice = DocType("POS Invoice")

	nts.qb.update(POSInvoice).set(POSInvoice.status, "Cancelled").where(POSInvoice.docstatus == 2).run()
