import nts
from nts.utils import today


def execute():
	for dt in ("cost_center_allocation", "cost_center_allocation_percentage"):
		nts.reload_doc("accounts", "doctype", dt)

	cc_allocations = get_existing_cost_center_allocations()
	if cc_allocations:
		create_new_cost_center_allocation_records(cc_allocations)

	nts.delete_doc("DocType", "Distributed Cost Center", ignore_missing=True)


def create_new_cost_center_allocation_records(cc_allocations):
	for main_cc, allocations in cc_allocations.items():
		cca = nts.new_doc("Cost Center Allocation")
		cca.main_cost_center = main_cc
		cca.valid_from = today()
		cca._skip_from_date_validation = True

		for child_cc, percentage in allocations.items():
			cca.append("allocation_percentages", ({"cost_center": child_cc, "percentage": percentage}))

		cca.save()
		cca.submit()


def get_existing_cost_center_allocations():
	if not nts.db.exists("DocType", "Distributed Cost Center"):
		return

	par = nts.qb.DocType("Cost Center")
	child = nts.qb.DocType("Distributed Cost Center")

	records = (
		nts.qb.from_(par)
		.inner_join(child)
		.on(par.name == child.parent)
		.select(par.name, child.cost_center, child.percentage_allocation)
		.where(par.enable_distributed_cost_center == 1)
	).run(as_dict=True)

	cc_allocations = nts._dict()
	for d in records:
		cc_allocations.setdefault(d.name, nts._dict()).setdefault(d.cost_center, d.percentage_allocation)

	return cc_allocations
