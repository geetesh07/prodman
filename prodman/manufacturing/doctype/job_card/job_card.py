# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import datetime
import json
from collections import OrderedDict

import nts
from nts import _, bold
from nts.model.document import Document
from nts.model.mapper import get_mapped_doc
from nts.query_builder import Criterion
from nts.query_builder.functions import IfNull, Max, Min
from nts.utils import (
	add_days,
	add_to_date,
	cint,
	flt,
	get_datetime,
	get_link_to_form,
	get_time,
	getdate,
	time_diff,
	time_diff_in_hours,
	time_diff_in_seconds,
)

from prodman.manufacturing.doctype.manufacturing_settings.manufacturing_settings import (
	get_mins_between_operations,
)
from prodman.manufacturing.doctype.workstation_type.workstation_type import get_workstations


class OverlapError(nts.ValidationError):
	pass


class OperationMismatchError(nts.ValidationError):
	pass


class OperationSequenceError(nts.ValidationError):
	pass


class JobCardCancelError(nts.ValidationError):
	pass


class JobCardOverTransferError(nts.ValidationError):
	pass


class JobCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from nts.types import DF

		from prodman.manufacturing.doctype.job_card_item.job_card_item import JobCardItem
		from prodman.manufacturing.doctype.job_card_operation.job_card_operation import JobCardOperation
		from prodman.manufacturing.doctype.job_card_scheduled_time.job_card_scheduled_time import (
			JobCardScheduledTime,
		)
		from prodman.manufacturing.doctype.job_card_scrap_item.job_card_scrap_item import JobCardScrapItem
		from prodman.manufacturing.doctype.job_card_time_log.job_card_time_log import JobCardTimeLog

		actual_end_date: DF.Datetime | None
		actual_start_date: DF.Datetime | None
		amended_from: DF.Link | None
		barcode: DF.Barcode | None
		batch_no: DF.Link | None
		bom_no: DF.Link | None
		company: DF.Link
		current_time: DF.Int
		employee: DF.TableMultiSelect[JobCardTimeLog]
		expected_end_date: DF.Datetime | None
		expected_start_date: DF.Datetime | None
		for_job_card: DF.Link | None
		for_operation: DF.Link | None
		for_quantity: DF.Float
		hour_rate: DF.Currency
		is_corrective_job_card: DF.Check
		item_name: DF.ReadOnly | None
		items: DF.Table[JobCardItem]
		job_started: DF.Check
		naming_series: DF.Literal["PO-JOB.#####"]
		operation: DF.Link
		operation_id: DF.Data | None
		operation_row_number: DF.Literal[None]
		posting_date: DF.Date | None
		process_loss_qty: DF.Float
		production_item: DF.Link | None
		project: DF.Link | None
		quality_inspection: DF.Link | None
		quality_inspection_template: DF.Link | None
		remarks: DF.SmallText | None
		requested_qty: DF.Float
		scheduled_time_logs: DF.Table[JobCardScheduledTime]
		scrap_items: DF.Table[JobCardScrapItem]
		sequence_id: DF.Int
		serial_and_batch_bundle: DF.Link | None
		serial_no: DF.SmallText | None
		started_time: DF.Datetime | None
		status: DF.Literal[
			"Open",
			"Work In Progress",
			"Material Transferred",
			"On Hold",
			"Submitted",
			"Cancelled",
			"Completed",
		]
		sub_operations: DF.Table[JobCardOperation]
		time_logs: DF.Table[JobCardTimeLog]
		time_required: DF.Float
		total_completed_qty: DF.Float
		total_time_in_mins: DF.Float
		transferred_qty: DF.Float
		wip_warehouse: DF.Link
		work_order: DF.Link
		workstation: DF.Link
		workstation_type: DF.Link | None
	# end: auto-generated types

	def onload(self):
		excess_transfer = nts.db.get_single_value("Manufacturing Settings", "job_card_excess_transfer")
		self.set_onload("job_card_excess_transfer", excess_transfer)
		self.set_onload("work_order_closed", self.is_work_order_closed())
		self.set_onload("has_stock_entry", self.has_stock_entry())

	def has_stock_entry(self):
		return nts.db.exists("Stock Entry", {"job_card": self.name, "docstatus": ["!=", 2]})

	def before_validate(self):
		self.set_wip_warehouse()

	def validate(self):
		self.validate_time_logs()
		self.set_status()
		self.validate_operation_id()
		self.validate_sequence_id()
		self.set_sub_operations()
		self.update_sub_operation_status()
		self.validate_work_order()

	def on_update(self):
		self.validate_job_card_qty()

	def validate_job_card_qty(self):
		if not (self.operation_id and self.work_order):
			return

		wo_qty = flt(nts.get_cached_value("Work Order", self.work_order, "qty"))

		completed_qty = flt(nts.db.get_value("Work Order Operation", self.operation_id, "completed_qty"))

		over_production_percentage = flt(
			nts.db.get_single_value("Manufacturing Settings", "overproduction_percentage_for_work_order")
		)

		wo_qty = wo_qty + (wo_qty * over_production_percentage / 100)

		job_card_qty = nts.get_all(
			"Job Card",
			fields=["sum(for_quantity)"],
			filters={
				"work_order": self.work_order,
				"operation_id": self.operation_id,
				"docstatus": ["!=", 2],
			},
			as_list=1,
		)

		job_card_qty = flt(job_card_qty[0][0]) if job_card_qty else 0

		if job_card_qty and ((job_card_qty - completed_qty) > wo_qty):
			form_link = get_link_to_form("Manufacturing Settings", "Manufacturing Settings")

			msg = f"""
				Qty To Manufacture in the job card
				cannot be greater than Qty To Manufacture in the
				work order for the operation {bold(self.operation)}.
				<br><br><b>Solution: </b> Either you can reduce the
				Qty To Manufacture in the job card or set the
				'Overproduction Percentage For Work Order'
				in the {form_link}."""

			nts.throw(_(msg), title=_("Extra Job Card Quantity"))

	def set_sub_operations(self):
		if not self.sub_operations and self.operation:
			self.sub_operations = []
			for row in nts.get_all(
				"Sub Operation",
				filters={"parent": self.operation},
				fields=["operation", "idx"],
				order_by="idx",
			):
				row.status = "Pending"
				row.sub_operation = row.operation
				self.append("sub_operations", row)

	def validate_time_logs(self):
		self.total_time_in_mins = 0.0
		self.total_completed_qty = 0.0

		if self.get("time_logs"):
			for d in self.get("time_logs"):
				if d.to_time and get_datetime(d.from_time) > get_datetime(d.to_time):
					nts.throw(_("Row {0}: From time must be less than to time").format(d.idx))

				open_job_cards = []
				if d.get("employee"):
					open_job_cards = self.get_open_job_cards(d.get("employee"), workstation=self.workstation)

				data = self.get_overlap_for(d, open_job_cards=open_job_cards)
				if data:
					nts.throw(
						_("Row {0}: From Time and To Time of {1} is overlapping with {2}").format(
							d.idx, self.name, data.name
						),
						OverlapError,
					)

				if d.from_time and d.to_time:
					d.time_in_mins = time_diff_in_hours(d.to_time, d.from_time) * 60
					self.total_time_in_mins += d.time_in_mins

				if d.completed_qty and not self.sub_operations:
					self.total_completed_qty += d.completed_qty

			self.total_completed_qty = flt(self.total_completed_qty, self.precision("total_completed_qty"))

		for row in self.sub_operations:
			self.total_completed_qty += row.completed_qty

	def get_overlap_for(self, args, open_job_cards=None):
		time_logs = []

		time_logs.extend(self.get_time_logs(args, "Job Card Time Log"))

		time_logs.extend(self.get_time_logs(args, "Job Card Scheduled Time", open_job_cards=open_job_cards))

		if not time_logs:
			return {}

		time_logs = sorted(time_logs, key=lambda x: x.get("to_time"))

		production_capacity = 1
		if self.workstation:
			production_capacity = (
				nts.get_cached_value("Workstation", self.workstation, "production_capacity") or 1
			)

		if self.get_open_job_cards(args.get("employee")):
			nts.throw(
				_(
					"Employee {0} is currently working on another workstation. Please assign another employee."
				).format(args.get("employee")),
				OverlapError,
			)

		if not self.has_overlap(production_capacity, time_logs):
			return {}

		if not self.workstation and self.workstation_type and time_logs:
			if workstation_time := self.get_workstation_based_on_available_slot(time_logs):
				self.workstation = workstation_time.get("workstation")
				return workstation_time

		return time_logs[0]

	def has_overlap(self, production_capacity, time_logs):
		overlap = False
		if production_capacity == 1 and len(time_logs) >= 1:
			return True
		if not len(time_logs):
			return False

		# sorting overlapping job cards as per from_time
		time_logs = sorted(time_logs, key=lambda x: x.get("from_time"))
		# alloted_capacity has key number starting from 1. Key number will increment by 1 if non sequential job card found
		# if key number reaches/crosses to production_capacity means capacity is full and overlap error generated
		# this will store last to_time of sequential job cards
		alloted_capacity = {1: time_logs[0]["to_time"]}
		# flag for sequential Job card found
		sequential_job_card_found = False
		for i in range(1, len(time_logs)):
			# scanning for all Existing keys
			for key in alloted_capacity.keys():
				# if current Job Card from time is greater than last to_time in that key means these job card are sequential
				if alloted_capacity[key] <= time_logs[i]["from_time"]:
					# So update key's value with last to_time
					alloted_capacity[key] = time_logs[i]["to_time"]
					# flag is true as we get sequential Job Card for that key
					sequential_job_card_found = True
					# Immediately break so that job card to time is not added with any other key except this
					break
			# if sequential job card not found above means it is overlapping  so increment key number to alloted_capacity
			if not sequential_job_card_found:
				# increment key number
				key = key + 1
				# for that key last to time is assigned.
				alloted_capacity[key] = time_logs[i]["to_time"]
		if len(alloted_capacity) >= production_capacity:
			# if number of keys greater or equal to production caoacity means full capacity is utilized and we should throw overlap error
			return True
		return overlap

	def get_time_logs(self, args, doctype, open_job_cards=None):
		if args.get("remaining_time_in_mins") and get_datetime(args.from_time) >= get_datetime(args.to_time):
			args.to_time = add_to_date(args.from_time, minutes=args.get("remaining_time_in_mins"))

		jc = nts.qb.DocType("Job Card")
		jctl = nts.qb.DocType(doctype)

		time_conditions = [
			((jctl.from_time < args.from_time) & (jctl.to_time > args.from_time)),
			((jctl.from_time < args.to_time) & (jctl.to_time > args.to_time)),
			((jctl.from_time >= args.from_time) & (jctl.to_time <= args.to_time)),
		]

		query = (
			nts.qb.from_(jctl)
			.from_(jc)
			.select(
				jc.name.as_("name"),
				jctl.name.as_("row_name"),
				jctl.from_time,
				jctl.to_time,
				jc.workstation,
				jc.workstation_type,
			)
			.where(
				(jctl.parent == jc.name)
				& (Criterion.any(time_conditions))
				& (jctl.name != f"{args.name or 'No Name'}")
				& (jc.name != f"{args.parent or 'No Name'}")
				& (jc.docstatus < 2)
			)
			.orderby(jctl.to_time)
		)

		if self.workstation_type:
			query = query.where(jc.workstation_type == self.workstation_type)

		if self.workstation:
			query = query.where(jc.workstation == self.workstation)

		if args.get("employee"):
			if not open_job_cards and doctype == "Job Card Scheduled Time":
				return []

			if doctype == "Job Card Time Log":
				query = query.where(jctl.employee == args.get("employee"))
			else:
				query = query.where(jc.name.isin(open_job_cards))

		if doctype == "Job Card Time Log":
			query = query.where(jc.docstatus < 2)
		else:
			query = query.where((jc.docstatus == 0) & (jc.total_time_in_mins == 0))

		time_logs = query.run(as_dict=True)

		return time_logs

	def get_open_job_cards(self, employee, workstation=None):
		jc = nts.qb.DocType("Job Card")
		jctl = nts.qb.DocType("Job Card Time Log")

		query = (
			nts.qb.from_(jc)
			.left_join(jctl)
			.on(jc.name == jctl.parent)
			.select(jc.name)
			.where(
				(jctl.parent == jc.name)
				& (jctl.employee == employee)
				& (jc.docstatus < 1)
				& (jc.name != self.name)
			)
		)

		if workstation:
			query = query.where(jc.workstation == workstation)

		jobs = query.run(as_dict=True)
		return [job.get("name") for job in jobs] if jobs else []

	def get_workstation_based_on_available_slot(self, existing_time_logs) -> dict:
		workstations = get_workstations(self.workstation_type)
		if workstations:
			busy_workstations = self.time_slot_wise_busy_workstations(existing_time_logs)
			for time_slot in busy_workstations:
				available_workstations = sorted(list(set(workstations) - set(busy_workstations[time_slot])))
				if available_workstations:
					return nts._dict(
						{
							"workstation": available_workstations[0],
							"planned_start_time": get_datetime(time_slot[0]),
							"to_time": get_datetime(time_slot[1]),
						}
					)

		return nts._dict({})

	@staticmethod
	def time_slot_wise_busy_workstations(existing_time_logs) -> dict:
		time_slot = OrderedDict()
		for row in existing_time_logs:
			from_time = get_datetime(row.from_time).strftime("%Y-%m-%d %H:%M")
			to_time = get_datetime(row.to_time).strftime("%Y-%m-%d %H:%M")
			time_slot.setdefault((from_time, to_time), []).append(row.workstation)

		return time_slot

	def schedule_time_logs(self, row):
		row.remaining_time_in_mins = row.time_in_mins
		while row.remaining_time_in_mins > 0:
			args = nts._dict(
				{
					"from_time": row.planned_start_time,
					"to_time": row.planned_end_time,
					"remaining_time_in_mins": row.remaining_time_in_mins,
				}
			)

			self.validate_overlap_for_workstation(args, row)
			self.check_workstation_time(row)

	def validate_overlap_for_workstation(self, args, row):
		# get the last record based on the to time from the job card
		data = self.get_overlap_for(args)

		if not self.workstation:
			workstations = get_workstations(self.workstation_type)
			if workstations:
				# Get the first workstation
				self.workstation = workstations[0]

		if not data:
			row.planned_start_time = args.from_time
			return

		if data:
			if data.get("planned_start_time"):
				args.planned_start_time = get_datetime(data.planned_start_time)
			else:
				args.planned_start_time = get_datetime(data.to_time + get_mins_between_operations())

			args.from_time = args.planned_start_time
			args.to_time = add_to_date(args.planned_start_time, minutes=row.remaining_time_in_mins)

			self.validate_overlap_for_workstation(args, row)

	def check_workstation_time(self, row):
		workstation_doc = nts.get_cached_doc("Workstation", self.workstation)
		if not workstation_doc.working_hours or cint(
			nts.db.get_single_value("Manufacturing Settings", "allow_overtime")
		):
			if get_datetime(row.planned_end_time) <= get_datetime(row.planned_start_time):
				row.planned_end_time = add_to_date(row.planned_start_time, minutes=row.time_in_mins)
				row.remaining_time_in_mins = 0.0
			else:
				row.remaining_time_in_mins -= time_diff_in_minutes(
					row.planned_end_time, row.planned_start_time
				)

			self.update_time_logs(row)
			return

		start_date = getdate(row.planned_start_time)
		start_time = get_time(row.planned_start_time)

		new_start_date = workstation_doc.validate_workstation_holiday(start_date)

		if new_start_date != start_date:
			row.planned_start_time = datetime.datetime.combine(new_start_date, start_time)
			start_date = new_start_date

		total_idx = len(workstation_doc.working_hours)

		for i, time_slot in enumerate(workstation_doc.working_hours):
			workstation_start_time = datetime.datetime.combine(start_date, get_time(time_slot.start_time))
			workstation_end_time = datetime.datetime.combine(start_date, get_time(time_slot.end_time))

			if (
				get_datetime(row.planned_start_time) >= workstation_start_time
				and get_datetime(row.planned_start_time) <= workstation_end_time
			):
				time_in_mins = time_diff_in_minutes(workstation_end_time, row.planned_start_time)

				# If remaining time fit in workstation time logs else split hours as per workstation time
				if time_in_mins > row.remaining_time_in_mins:
					row.planned_end_time = add_to_date(
						row.planned_start_time, minutes=row.remaining_time_in_mins
					)
					row.remaining_time_in_mins = 0
				else:
					row.planned_end_time = add_to_date(row.planned_start_time, minutes=time_in_mins)
					row.remaining_time_in_mins -= time_in_mins

				self.update_time_logs(row)

				if total_idx != (i + 1) and row.remaining_time_in_mins > 0:
					row.planned_start_time = datetime.datetime.combine(
						start_date, get_time(workstation_doc.working_hours[i + 1].start_time)
					)

		if row.remaining_time_in_mins > 0:
			start_date = add_days(start_date, 1)
			row.planned_start_time = datetime.datetime.combine(
				start_date, get_time(workstation_doc.working_hours[0].start_time)
			)

	def add_time_log(self, args):
		last_row = []
		employees = args.employees
		if isinstance(employees, str):
			employees = json.loads(employees)

		if self.time_logs and len(self.time_logs) > 0:
			last_row = self.time_logs[-1]

		self.reset_timer_value(args)
		if last_row and args.get("complete_time"):
			for row in self.time_logs:
				if not row.to_time:
					row.update(
						{
							"to_time": get_datetime(args.get("complete_time")),
							"operation": args.get("sub_operation"),
							"completed_qty": (args.get("completed_qty") if last_row.idx == row.idx else 0.0),
						}
					)
		elif args.get("start_time"):
			new_args = nts._dict(
				{
					"from_time": get_datetime(args.get("start_time")),
					"operation": args.get("sub_operation"),
					"completed_qty": 0.0,
				}
			)

			if employees:
				for name in employees:
					new_args.employee = name.get("employee")
					self.add_start_time_log(new_args)
			else:
				self.add_start_time_log(new_args)

		if not self.employee and employees:
			self.set_employees(employees)

		if self.status == "On Hold":
			self.current_time = time_diff_in_seconds(last_row.to_time, last_row.from_time)

		self.save()

	def add_start_time_log(self, args):
		self.append("time_logs", args)

	def set_employees(self, employees):
		for name in employees:
			self.append("employee", {"employee": name.get("employee"), "completed_qty": 0.0})

	def reset_timer_value(self, args):
		self.started_time = None

		if args.get("status") in ["Work In Progress", "Complete"]:
			self.current_time = 0.0

			if args.get("status") == "Work In Progress":
				self.started_time = get_datetime(args.get("start_time"))

		if args.get("status") == "Resume Job":
			args["status"] = "Work In Progress"

		if args.get("status"):
			self.status = args.get("status")

	def update_sub_operation_status(self):
		if not (self.sub_operations and self.time_logs):
			return

		operation_wise_completed_time = {}
		for time_log in self.time_logs:
			if time_log.operation not in operation_wise_completed_time:
				operation_wise_completed_time.setdefault(
					time_log.operation,
					nts._dict(
						{"status": "Pending", "completed_qty": 0.0, "completed_time": 0.0, "employee": []}
					),
				)

			op_row = operation_wise_completed_time[time_log.operation]
			op_row.status = "Work In Progress" if not time_log.time_in_mins else "Complete"
			if self.status == "On Hold":
				op_row.status = "Pause"

			op_row.employee.append(time_log.employee)
			if time_log.time_in_mins:
				op_row.completed_time += time_log.time_in_mins
				op_row.completed_qty += time_log.completed_qty

		for row in self.sub_operations:
			operation_deatils = operation_wise_completed_time.get(row.sub_operation)
			if operation_deatils:
				if row.status != "Complete":
					row.status = operation_deatils.status

				row.completed_time = operation_deatils.completed_time
				if operation_deatils.employee:
					row.completed_time = row.completed_time / len(set(operation_deatils.employee))

					if operation_deatils.completed_qty:
						row.completed_qty = operation_deatils.completed_qty / len(
							set(operation_deatils.employee)
						)
			else:
				row.status = "Pending"
				row.completed_time = 0.0
				row.completed_qty = 0.0

	def update_time_logs(self, row):
		self.append(
			"scheduled_time_logs",
			{
				"from_time": row.planned_start_time,
				"to_time": row.planned_end_time,
				"completed_qty": 0,
				"time_in_mins": time_diff_in_minutes(row.planned_end_time, row.planned_start_time),
			},
		)

	@nts.whitelist()
	def get_required_items(self):
		if not self.get("work_order"):
			return

		doc = nts.get_doc("Work Order", self.get("work_order"))
		if doc.transfer_material_against == "Work Order" or doc.skip_transfer:
			return

		for d in doc.required_items:
			if not d.operation:
				nts.throw(
					_("Row {0} : Operation is required against the raw material item {1}").format(
						d.idx, d.item_code
					)
				)

			if self.get("operation") == d.operation or self.is_corrective_job_card:
				self.append(
					"items",
					{
						"item_code": d.item_code,
						"source_warehouse": d.source_warehouse,
						"uom": nts.db.get_value("Item", d.item_code, "stock_uom"),
						"item_name": d.item_name,
						"description": d.description,
						"required_qty": (d.required_qty * flt(self.for_quantity)) / doc.qty,
						"rate": d.rate,
						"amount": d.amount,
					},
				)

	def before_save(self):
		self.set_expected_and_actual_time()
		self.set_process_loss()

	def on_submit(self):
		self.validate_transfer_qty()
		self.validate_job_card()
		self.update_work_order()
		self.set_transferred_qty()

	def on_cancel(self):
		self.update_work_order()
		self.set_transferred_qty()

	def validate_transfer_qty(self):
		if not self.is_corrective_job_card and self.items and self.transferred_qty < self.for_quantity:
			nts.throw(
				_(
					"Materials needs to be transferred to the work in progress warehouse for the job card {0}"
				).format(self.name)
			)

	def validate_job_card(self):
		if self.work_order and nts.get_cached_value("Work Order", self.work_order, "status") == "Stopped":
			nts.throw(
				_("Transaction not allowed against stopped Work Order {0}").format(
					get_link_to_form("Work Order", self.work_order)
				)
			)

		if not self.time_logs:
			nts.throw(
				_("Time logs are required for {0} {1}").format(
					bold("Job Card"), get_link_to_form("Job Card", self.name)
				)
			)
		elif nts.db.get_single_value("Manufacturing Settings", "enforce_time_logs"):
			for row in self.time_logs:
				if not row.from_time or not row.to_time:
					nts.throw(
						_("Row #{0}: From Time and To Time fields are required").format(row.idx),
					)

		precision = self.precision("total_completed_qty")
		total_completed_qty = flt(
			flt(self.total_completed_qty, precision) + flt(self.process_loss_qty, precision)
		)

		if self.for_quantity and flt(total_completed_qty, precision) != flt(self.for_quantity, precision):
			total_completed_qty_label = bold(_("Total Completed Qty"))
			qty_to_manufacture = bold(_("Qty to Manufacture"))

			nts.throw(
				_("The {0} ({1}) must be equal to {2} ({3})").format(
					total_completed_qty_label,
					bold(flt(total_completed_qty, precision)),
					qty_to_manufacture,
					bold(self.for_quantity),
				)
			)

	def set_expected_and_actual_time(self):
		for child_table, start_field, end_field, time_required in [
			("scheduled_time_logs", "expected_start_date", "expected_end_date", "time_required"),
			("time_logs", "actual_start_date", "actual_end_date", "total_time_in_mins"),
		]:
			if not self.get(child_table):
				continue

			time_list = []
			time_in_mins = 0.0
			for row in self.get(child_table):
				time_in_mins += flt(row.get("time_in_mins"))
				for field in ["from_time", "to_time"]:
					if row.get(field):
						time_list.append(get_datetime(row.get(field)))

			if time_list:
				self.set(start_field, min(time_list))
				if end_field == "actual_end_date" and not self.time_logs[-1].to_time:
					self.set(end_field, "")
					return

				self.set(end_field, max(time_list))

			self.set(time_required, time_in_mins)

	def set_process_loss(self):
		precision = self.precision("total_completed_qty")

		self.process_loss_qty = 0.0
		if self.total_completed_qty and self.for_quantity > self.total_completed_qty:
			self.process_loss_qty = flt(self.for_quantity, precision) - flt(
				self.total_completed_qty, precision
			)

	def update_work_order(self):
		if not self.work_order:
			return

		if self.is_corrective_job_card and not cint(
			nts.db.get_single_value(
				"Manufacturing Settings", "add_corrective_operation_cost_in_finished_good_valuation"
			)
		):
			return

		for_quantity, time_in_mins, process_loss_qty = 0, 0, 0
		_from_time_list, _to_time_list = [], []

		data = self.get_current_operation_data()
		if data and len(data) > 0:
			for_quantity = flt(data[0].completed_qty)
			time_in_mins = flt(data[0].time_in_mins)
			process_loss_qty = flt(data[0].process_loss_qty)

		wo = nts.get_doc("Work Order", self.work_order)

		if self.is_corrective_job_card:
			self.update_corrective_in_work_order(wo)

		elif self.operation_id:
			self.validate_produced_quantity(for_quantity, process_loss_qty, wo)
			self.update_work_order_data(for_quantity, process_loss_qty, time_in_mins, wo)

	def update_corrective_in_work_order(self, wo):
		wo.corrective_operation_cost = 0.0
		for row in nts.get_all(
			"Job Card",
			fields=["total_time_in_mins", "hour_rate"],
			filters={"is_corrective_job_card": 1, "docstatus": 1, "work_order": self.work_order},
		):
			wo.corrective_operation_cost += (flt(row.total_time_in_mins) / 60) * flt(row.hour_rate)

		wo.calculate_operating_cost()
		wo.flags.ignore_validate_update_after_submit = True
		wo.save()

	def validate_produced_quantity(self, for_quantity, process_loss_qty, wo):
		if self.docstatus < 2:
			return

		if wo.produced_qty > for_quantity + process_loss_qty:
			first_part_msg = _(
				"The {0} {1} is used to calculate the valuation cost for the finished good {2}."
			).format(nts.bold(_("Job Card")), nts.bold(self.name), nts.bold(self.production_item))

			second_part_msg = _(
				"Kindly cancel the Manufacturing Entries first against the work order {0}."
			).format(nts.bold(get_link_to_form("Work Order", self.work_order)))

			nts.throw(
				_("{0} {1}").format(first_part_msg, second_part_msg), JobCardCancelError, title=_("Error")
			)

	def update_work_order_data(self, for_quantity, process_loss_qty, time_in_mins, wo):
		workstation_hour_rate = nts.get_value("Workstation", self.workstation, "hour_rate")
		jc = nts.qb.DocType("Job Card")
		jctl = nts.qb.DocType("Job Card Time Log")

		time_data = (
			nts.qb.from_(jc)
			.from_(jctl)
			.select(Min(jctl.from_time).as_("start_time"), Max(jctl.to_time).as_("end_time"))
			.where(
				(jctl.parent == jc.name)
				& (jc.work_order == self.work_order)
				& (jc.operation_id == self.operation_id)
				& (jc.docstatus == 1)
				& (IfNull(jc.is_corrective_job_card, 0) == 0)
			)
		).run(as_dict=True)

		for data in wo.operations:
			if data.get("name") == self.operation_id:
				data.completed_qty = for_quantity
				data.process_loss_qty = process_loss_qty
				data.actual_operation_time = time_in_mins
				data.actual_start_time = time_data[0].start_time if time_data else None
				data.actual_end_time = time_data[0].end_time if time_data else None
				if data.get("workstation") != self.workstation:
					# workstations can change in a job card
					data.workstation = self.workstation
					data.hour_rate = flt(workstation_hour_rate)

		wo.flags.ignore_validate_update_after_submit = True
		wo.update_operation_status()
		wo.calculate_operating_cost()
		wo.set_actual_dates()
		wo.save()

	def get_current_operation_data(self):
		return nts.get_all(
			"Job Card",
			fields=[
				"sum(total_time_in_mins) as time_in_mins",
				"sum(total_completed_qty) as completed_qty",
				"sum(process_loss_qty) as process_loss_qty",
			],
			filters={
				"docstatus": 1,
				"work_order": self.work_order,
				"operation_id": self.operation_id,
				"is_corrective_job_card": 0,
			},
		)

	def set_transferred_qty_in_job_card_item(self, ste_doc):
		def _get_job_card_items_transferred_qty(ste_doc):
			from nts.query_builder.functions import Sum

			job_card_items_transferred_qty = {}
			job_card_items = [x.get("job_card_item") for x in ste_doc.get("items") if x.get("job_card_item")]

			if job_card_items:
				se = nts.qb.DocType("Stock Entry")
				sed = nts.qb.DocType("Stock Entry Detail")

				query = (
					nts.qb.from_(sed)
					.join(se)
					.on(sed.parent == se.name)
					.select(sed.job_card_item, Sum(sed.qty))
					.where(
						(sed.job_card_item.isin(job_card_items))
						& (se.docstatus == 1)
						& (se.purpose == "Material Transfer for Manufacture")
					)
					.groupby(sed.job_card_item)
				)

				job_card_items_transferred_qty = nts._dict(query.run(as_list=True))

			return job_card_items_transferred_qty

		def _validate_over_transfer(row, transferred_qty):
			"Block over transfer of items if not allowed in settings."
			required_qty = nts.db.get_value("Job Card Item", row.job_card_item, "required_qty")
			is_excess = flt(transferred_qty) > flt(required_qty)
			if is_excess:
				nts.throw(
					_(
						"Row #{0}: Cannot transfer more than Required Qty {1} for Item {2} against Job Card {3}"
					).format(
						row.idx, nts.bold(required_qty), nts.bold(row.item_code), ste_doc.job_card
					),
					title=_("Excess Transfer"),
					exc=JobCardOverTransferError,
				)

		job_card_items_transferred_qty = _get_job_card_items_transferred_qty(ste_doc) or {}
		allow_excess = nts.db.get_single_value("Manufacturing Settings", "job_card_excess_transfer")

		for row in ste_doc.items:
			if not row.job_card_item:
				continue

			transferred_qty = flt(job_card_items_transferred_qty.get(row.job_card_item, 0.0))

			if not allow_excess:
				_validate_over_transfer(row, transferred_qty)

			nts.db.set_value("Job Card Item", row.job_card_item, "transferred_qty", flt(transferred_qty))

	def set_transferred_qty(self, update_status=False):
		"Set total FG Qty in Job Card for which RM was transferred."
		if not self.items:
			self.transferred_qty = self.for_quantity if self.docstatus == 1 else 0

		doc = nts.get_doc("Work Order", self.get("work_order"))
		if doc.transfer_material_against == "Work Order" or doc.skip_transfer:
			return

		if self.items:
			# sum of 'For Quantity' of Stock Entries against JC
			self.transferred_qty = (
				nts.db.get_value(
					"Stock Entry",
					{
						"job_card": self.name,
						"work_order": self.work_order,
						"docstatus": 1,
						"purpose": "Material Transfer for Manufacture",
					},
					"sum(fg_completed_qty)",
				)
				or 0
			)

		self.db_set("transferred_qty", self.transferred_qty)

		qty = 0
		if self.work_order:
			if doc.transfer_material_against == "Job Card" and not doc.skip_transfer:
				min_qty = []
				for d in doc.operations:
					completed_qty = flt(d.completed_qty) + flt(d.process_loss_qty)
					if completed_qty:
						min_qty.append(completed_qty)
					else:
						min_qty = []
						break

				if min_qty:
					qty = min(min_qty)

				doc.db_set("material_transferred_for_manufacturing", qty)

		self.set_status(update_status)

	def set_status(self, update_status=False):
		if self.status == "On Hold" and self.docstatus == 0:
			return

		self.status = {0: "Open", 1: "Submitted", 2: "Cancelled"}[self.docstatus or 0]

		if self.docstatus < 2:
			if flt(self.for_quantity) <= flt(self.transferred_qty):
				self.status = "Material Transferred"

			if self.time_logs:
				self.status = "Work In Progress"

			if self.docstatus == 1 and (
				self.for_quantity <= (self.total_completed_qty + self.process_loss_qty) or not self.items
			):
				self.status = "Completed"

		if update_status:
			self.db_set("status", self.status)

		if self.status in ["Completed", "Work In Progress"]:
			status = {
				"Completed": "Off",
				"Work In Progress": "Production",
			}.get(self.status)

			self.update_status_in_workstation(status)

	def set_wip_warehouse(self):
		if not self.wip_warehouse:
			self.wip_warehouse = nts.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")

	def validate_operation_id(self):
		if (
			self.get("operation_id")
			and self.get("operation_row_number")
			and self.operation
			and self.work_order
			and nts.get_cached_value("Work Order Operation", self.operation_row_number, "name")
			!= self.operation_id
		):
			work_order = bold(get_link_to_form("Work Order", self.work_order))
			nts.throw(
				_("Operation {0} does not belong to the work order {1}").format(
					bold(self.operation), work_order
				),
				OperationMismatchError,
			)

	def validate_sequence_id(self):
		if self.is_corrective_job_card:
			return

		if not (self.work_order and self.sequence_id):
			return

		current_operation_qty = 0.0
		data = self.get_current_operation_data()
		if data and len(data) > 0:
			current_operation_qty = flt(data[0].completed_qty)

		current_operation_qty += flt(self.total_completed_qty)

		data = nts.get_all(
			"Work Order Operation",
			fields=["operation", "status", "completed_qty", "sequence_id"],
			filters={"docstatus": 1, "parent": self.work_order, "sequence_id": ("<", self.sequence_id)},
			order_by="sequence_id, idx",
		)

		message = "Job Card {}: As per the sequence of the operations in the work order {}".format(
			bold(self.name), bold(get_link_to_form("Work Order", self.work_order))
		)

		for row in data:
			if row.status != "Completed" and row.completed_qty < current_operation_qty:
				nts.throw(
					_("{0}, complete the operation {1} before the operation {2}.").format(
						message, bold(row.operation), bold(self.operation)
					),
					OperationSequenceError,
				)

			if row.completed_qty < current_operation_qty:
				msg = f"""The completed quantity {bold(current_operation_qty)}
					of an operation {bold(self.operation)} cannot be greater
					than the completed quantity {bold(row.completed_qty)}
					of a previous operation
					{bold(row.operation)}.
				"""

				nts.throw(_(msg))

	def validate_work_order(self):
		if self.is_work_order_closed():
			nts.throw(_("You can't make any changes to Job Card since Work Order is closed."))

	def is_work_order_closed(self):
		if self.work_order:
			status = nts.get_value("Work Order", self.work_order)

			if status == "Closed":
				return True

		return False

	def update_status_in_workstation(self, status):
		if not self.workstation:
			return

		nts.db.set_value("Workstation", self.workstation, "status", status)


@nts.whitelist()
def make_time_log(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = nts._dict(args)
	doc = nts.get_doc("Job Card", args.job_card_id)
	doc.validate_sequence_id()
	doc.add_time_log(args)


@nts.whitelist()
def get_operation_details(work_order, operation):
	if work_order and operation:
		return nts.get_all(
			"Work Order Operation",
			fields=["name", "idx"],
			filters={"parent": work_order, "operation": operation},
		)


@nts.whitelist()
def get_operations(doctype, txt, searchfield, start, page_len, filters):
	if not filters.get("work_order"):
		nts.msgprint(_("Please select a Work Order first."))
		return []
	args = {"parent": filters.get("work_order")}
	if txt:
		args["operation"] = ("like", f"%{txt}%")

	return nts.get_all(
		"Work Order Operation",
		filters=args,
		fields=["distinct operation as operation"],
		limit_start=start,
		limit_page_length=page_len,
		order_by="idx asc",
		as_list=1,
	)


@nts.whitelist()
def make_material_request(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.warehouse = source_parent.wip_warehouse

	def set_missing_values(source, target):
		target.material_request_type = "Material Transfer"

	doclist = get_mapped_doc(
		"Job Card",
		source_name,
		{
			"Job Card": {
				"doctype": "Material Request",
				"field_map": {
					"name": "job_card",
				},
			},
			"Job Card Item": {
				"doctype": "Material Request Item",
				"field_map": {"required_qty": "qty", "uom": "stock_uom", "name": "job_card_item"},
				"postprocess": update_item,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist


@nts.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def update_item(source, target, source_parent):
		target.t_warehouse = source_parent.wip_warehouse

		if not target.conversion_factor:
			target.conversion_factor = 1

		pending_rm_qty = flt(source.required_qty) - flt(source.transferred_qty)
		if pending_rm_qty > 0:
			target.qty = pending_rm_qty

	def set_missing_values(source, target):
		target.purpose = "Material Transfer for Manufacture"
		target.from_bom = 1

		# avoid negative 'For Quantity'
		pending_fg_qty = flt(source.get("for_quantity", 0)) - flt(source.get("transferred_qty", 0))
		target.fg_completed_qty = pending_fg_qty if pending_fg_qty > 0 else 0

		target.set_missing_values()
		target.set_stock_entry_type()

		wo_allows_alternate_item = nts.db.get_value(
			"Work Order", target.work_order, "allow_alternative_item"
		)
		for item in target.items:
			item.allow_alternative_item = int(
				wo_allows_alternate_item
				and nts.get_cached_value("Item", item.item_code, "allow_alternative_item")
			)

	doclist = get_mapped_doc(
		"Job Card",
		source_name,
		{
			"Job Card": {
				"doctype": "Stock Entry",
				"field_map": {"name": "job_card", "for_quantity": "fg_completed_qty"},
			},
			"Job Card Item": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"source_warehouse": "s_warehouse",
					"required_qty": "qty",
					"name": "job_card_item",
				},
				"postprocess": update_item,
				"condition": lambda doc: doc.required_qty > 0,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist


def time_diff_in_minutes(string_ed_date, string_st_date):
	return time_diff(string_ed_date, string_st_date).total_seconds() / 60


@nts.whitelist()
def get_job_details(start, end, filters=None):
	events = []

	event_color = {
		"Completed": "#cdf5a6",
		"Material Transferred": "#ffdd9e",
		"Work In Progress": "#D3D3D3",
	}

	from nts.desk.reportview import get_filters_cond

	conditions = get_filters_cond("Job Card", filters, [])

	job_cards = nts.db.sql(
		f""" SELECT `tabJob Card`.name, `tabJob Card`.work_order,
			`tabJob Card`.status, ifnull(`tabJob Card`.remarks, ''),
			min(`tabJob Card Time Log`.from_time) as from_time,
			max(`tabJob Card Time Log`.to_time) as to_time
		FROM `tabJob Card` , `tabJob Card Time Log`
		WHERE
			`tabJob Card`.name = `tabJob Card Time Log`.parent {conditions}
			group by `tabJob Card`.name""",
		as_dict=1,
	)

	for d in job_cards:
		subject_data = []
		for field in ["name", "work_order", "remarks"]:
			if not d.get(field):
				continue

			subject_data.append(d.get(field))

		color = event_color.get(d.status)
		job_card_data = {
			"from_time": d.from_time,
			"to_time": d.to_time,
			"name": d.name,
			"subject": "\n".join(subject_data),
			"color": color if color else "#89bcde",
		}

		events.append(job_card_data)

	return events


@nts.whitelist()
def make_corrective_job_card(source_name, operation=None, for_operation=None, target_doc=None):
	def set_missing_values(source, target):
		target.is_corrective_job_card = 1
		target.operation = operation
		target.for_operation = for_operation

		target.set("time_logs", [])
		target.set("employee", [])
		target.set("items", [])
		target.set("sub_operations", [])
		target.set_sub_operations()
		target.get_required_items()
		target.validate_time_logs()

	doclist = get_mapped_doc(
		"Job Card",
		source_name,
		{
			"Job Card": {
				"doctype": "Job Card",
				"field_map": {
					"name": "for_job_card",
				},
			}
		},
		target_doc,
		set_missing_values,
	)

	return doclist
