import nts
from nts.model.db_query import DatabaseQuery
from nts.utils import cint, flt

from prodman.stock.doctype.stock_reservation_entry.stock_reservation_entry import (
	get_sre_reserved_qty_for_items_and_warehouses as get_reserved_stock_details,
)


@nts.whitelist()
def get_data(
	item_code=None, warehouse=None, item_group=None, start=0, sort_by="actual_qty", sort_order="desc"
):
	"""Return data to render the item dashboard"""
	filters = []
	if item_code:
		filters.append(["item_code", "=", item_code])
	if warehouse:
		filters.append(["warehouse", "=", warehouse])
	if item_group:
		lft, rgt = nts.db.get_value("Item Group", item_group, ["lft", "rgt"])
		items = nts.db.sql_list(
			"""
			select i.name from `tabItem` i
			where exists(select name from `tabItem Group`
				where name=i.item_group and lft >=%s and rgt<=%s)
		""",
			(lft, rgt),
		)
		filters.append(["item_code", "in", items])
	try:
		# check if user has any restrictions based on user permissions on warehouse
		if DatabaseQuery("Warehouse", user=nts.session.user).build_match_conditions():
			filters.append(["warehouse", "in", [w.name for w in nts.get_list("Warehouse")]])
	except nts.PermissionError:
		# user does not have access on warehouse
		return []

	items = nts.db.get_all(
		"Bin",
		fields=[
			"item_code",
			"warehouse",
			"projected_qty",
			"reserved_qty",
			"reserved_qty_for_production",
			"reserved_qty_for_sub_contract",
			"actual_qty",
			"valuation_rate",
		],
		or_filters={
			"projected_qty": ["!=", 0],
			"reserved_qty": ["!=", 0],
			"reserved_qty_for_production": ["!=", 0],
			"reserved_qty_for_sub_contract": ["!=", 0],
			"actual_qty": ["!=", 0],
		},
		filters=filters,
		order_by=sort_by + " " + sort_order,
		limit_start=start,
		limit_page_length=21,
	)

	item_code_list = [item_code] if item_code else [i.item_code for i in items]
	warehouse_list = [warehouse] if warehouse else [i.warehouse for i in items]

	sre_reserved_stock_details = get_reserved_stock_details(item_code_list, warehouse_list)
	precision = cint(nts.db.get_single_value("System Settings", "float_precision"))

	for item in items:
		item.update(
			{
				"item_name": nts.get_cached_value("Item", item.item_code, "item_name"),
				"stock_uom": nts.get_cached_value("Item", item.item_code, "stock_uom"),
				"disable_quick_entry": nts.get_cached_value("Item", item.item_code, "has_batch_no")
				or nts.get_cached_value("Item", item.item_code, "has_serial_no"),
				"projected_qty": flt(item.projected_qty, precision),
				"reserved_qty": flt(item.reserved_qty, precision),
				"reserved_qty_for_production": flt(item.reserved_qty_for_production, precision),
				"reserved_qty_for_sub_contract": flt(item.reserved_qty_for_sub_contract, precision),
				"actual_qty": flt(item.actual_qty, precision),
				"reserved_stock": flt(sre_reserved_stock_details.get((item.item_code, item.warehouse))),
			}
		)

	return items
