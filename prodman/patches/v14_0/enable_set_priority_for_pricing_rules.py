import nts


def execute():
	pr_table = nts.qb.DocType("Pricing Rule")
	(
		nts.qb.update(pr_table)
		.set(pr_table.has_priority, 1)
		.where((pr_table.priority.isnotnull()) & (pr_table.priority != ""))
	).run()
