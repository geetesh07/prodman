# Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import json
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
	from prodman.manufacturing.doctype.bom_update_log.bom_update_log import BOMUpdateLog

import nts
from nts.model.document import Document
from nts.utils import date_diff, get_datetime, now


class BOMUpdateTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		current_bom: DF.Link
		new_bom: DF.Link
	# end: auto-generated types

	pass


@nts.whitelist()
def enqueue_replace_bom(boms: dict | str | None = None, args: dict | str | None = None) -> "BOMUpdateLog":
	"""Returns a BOM Update Log (that queues a job) for BOM Replacement."""
	boms = boms or args
	if isinstance(boms, str):
		boms = json.loads(boms)

	update_log = create_bom_update_log(boms=boms)
	return update_log


@nts.whitelist()
def enqueue_update_cost() -> "BOMUpdateLog":
	"""Returns a BOM Update Log (that queues a job) for BOM Cost Updation."""
	update_log = create_bom_update_log(update_type="Update Cost")
	return update_log


def auto_update_latest_price_in_all_boms() -> None:
	"""Called via hooks.py."""
	if nts.db.get_single_value("Manufacturing Settings", "update_bom_costs_automatically"):
		wip_log = nts.get_all(
			"BOM Update Log",
			fields=["creation", "status"],
			filters={"update_type": "Update Cost", "status": ["in", ["Queued", "In Progress"]]},
			limit_page_length=1,
			order_by="creation desc",
		)

		if not wip_log or is_older_log(wip_log[0]):
			create_bom_update_log(update_type="Update Cost")


def is_older_log(log: dict) -> bool:
	no_of_days = date_diff(get_datetime(now()), get_datetime(log.creation))
	return no_of_days > 10


def create_bom_update_log(
	boms: dict[str, str] | None = None,
	update_type: Literal["Replace BOM", "Update Cost"] = "Replace BOM",
) -> "BOMUpdateLog":
	"""Creates a BOM Update Log that handles the background job."""

	boms = boms or {}
	current_bom = boms.get("current_bom")
	new_bom = boms.get("new_bom")
	return nts.get_doc(
		{
			"doctype": "BOM Update Log",
			"current_bom": current_bom,
			"new_bom": new_bom,
			"update_type": update_type,
		}
	).submit()
