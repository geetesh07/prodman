# Copyright (c) 2013, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.query_builder.functions import Date


def execute(filters=None):
	validate_filters(filters)

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def validate_filters(filters):
	if not filters:
		nts.throw(_("Please select the required filters"))

	if not filters.get("from_date"):
		nts.throw(_("'From Date' is required"))

	if not filters.get("to_date"):
		nts.throw(_("'To Date' is required"))


def get_columns():
	return [
		_("Item") + ":Link/Item:150",
		_("Item Name") + "::150",
		_("Batch") + ":Link/Batch:150",
		_("Stock UOM") + ":Link/UOM:100",
		_("Quantity") + ":Float:100",
		_("Expires On") + ":Date:100",
		_("Expiry (In Days)") + ":Int:130",
	]


def get_data(filters):
	data = []

	for batch in get_batch_details(filters):
		data.append(
			[
				batch.item,
				batch.item_name,
				batch.name,
				batch.stock_uom,
				batch.batch_qty,
				batch.expiry_date,
				max((batch.expiry_date - nts.utils.datetime.date.today()).days, 0)
				if batch.expiry_date
				else None,
			]
		)

	return data


def get_batch_details(filters):
	batch = nts.qb.DocType("Batch")
	query = (
		nts.qb.from_(batch)
		.select(
			batch.name,
			batch.creation,
			batch.expiry_date,
			batch.item,
			batch.item_name,
			batch.stock_uom,
			batch.batch_qty,
		)
		.where(
			(batch.disabled == 0)
			& (batch.batch_qty > 0)
			& ((Date(batch.creation) >= filters["from_date"]) & (Date(batch.creation) <= filters["to_date"]))
		)
		.orderby(batch.creation)
	)

	if filters.get("item"):
		query = query.where(batch.item == filters["item"])

	return query.run(as_dict=True)
