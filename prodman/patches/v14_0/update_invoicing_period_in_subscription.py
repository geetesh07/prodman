import nts


def execute():
	subscription = nts.qb.DocType("Subscription")
	nts.qb.update(subscription).set(
		subscription.generate_invoice_at, "Beginning of the current subscription period"
	).where(subscription.generate_invoice_at_period_start == 1).run()
