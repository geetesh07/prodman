import nts


def execute():
	nts.reload_doc("manufacturing", "doctype", "bom_operation")
	nts.reload_doc("manufacturing", "doctype", "work_order_operation")

	nts.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	nts.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
