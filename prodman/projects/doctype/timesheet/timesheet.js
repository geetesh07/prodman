// Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Timesheet", {
	setup: function (frm) {
		nts.require("/assets/prodman/js/projects/timer.js");

		frm.ignore_doctypes_on_cancel_all = ["Sales Invoice"];

		frm.fields_dict.employee.get_query = function () {
			return {
				filters: {
					status: "Active",
				},
			};
		};

		frm.fields_dict["time_logs"].grid.get_field("task").get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					project: child.project,
					status: ["!=", "Cancelled"],
				},
			};
		};

		frm.fields_dict["time_logs"].grid.get_field("project").get_query = function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		};
	},

	onload: function (frm) {
		if (frm.doc.__islocal && frm.doc.time_logs) {
			calculate_time_and_amount(frm);
		}

		if (frm.is_new() && !frm.doc.employee) {
			set_employee_and_company(frm);
		}
	},

	refresh: function (frm) {
		if (frm.doc.docstatus == 1) {
			if (
				frm.doc.per_billed < 100 &&
				frm.doc.total_billable_hours &&
				frm.doc.total_billable_hours > frm.doc.total_billed_hours
			) {
				frm.add_custom_button(__("Create Sales Invoice"), function () {
					frm.trigger("make_invoice");
				});
			}
		}

		if (frm.doc.docstatus < 1) {
			let button = __("Start Timer");
			$.each(frm.doc.time_logs || [], function (i, row) {
				if (row.from_time <= nts.datetime.now_datetime() && !row.completed) {
					button = __("Resume Timer");
				}
			});

			frm.add_custom_button(__(button), function () {
				var flag = true;
				$.each(frm.doc.time_logs || [], function (i, row) {
					// Fetch the row for which from_time is not present
					if (flag && row.activity_type && !row.from_time) {
						prodman.timesheet.timer(frm, row);
						row.from_time = nts.datetime.now_datetime();
						frm.refresh_fields("time_logs");
						frm.save();
						flag = false;
					}
					// Fetch the row for timer where activity is not completed and from_time is before now_time
					if (flag && row.from_time <= nts.datetime.now_datetime() && !row.completed) {
						let timestamp = moment(nts.datetime.now_datetime()).diff(
							moment(row.from_time),
							"seconds"
						);
						prodman.timesheet.timer(frm, row, timestamp);
						flag = false;
					}
				});
				// If no activities found to start a timer, create new
				if (flag) {
					prodman.timesheet.timer(frm);
				}
			}).addClass("btn-primary");
		}
		if (frm.doc.per_billed > 0) {
			frm.fields_dict["time_logs"].grid.toggle_enable("billing_hours", false);
			frm.fields_dict["time_logs"].grid.toggle_enable("is_billable", false);
		}

		let filters = {
			status: "Open",
		};

		if (frm.doc.customer) {
			filters["customer"] = frm.doc.customer;
		}

		frm.set_query("parent_project", function (doc) {
			return {
				filters: filters,
			};
		});

		frm.trigger("setup_filters");
		frm.trigger("set_dynamic_field_label");
		frm.trigger("set_route_options_for_new_task");
	},

	customer: function (frm) {
		frm.set_query("project", "time_logs", function (doc) {
			return {
				filters: {
					customer: doc.customer,
				},
			};
		});
		frm.refresh();
	},

	currency: function (frm) {
		let base_currency = nts.defaults.get_global_default("currency");
		if (frm.doc.currency && base_currency != frm.doc.currency) {
			nts.call({
				method: "prodman.setup.utils.get_exchange_rate",
				args: {
					from_currency: frm.doc.currency,
					to_currency: base_currency,
				},
				callback: function (r) {
					if (r.message) {
						frm.set_value("exchange_rate", flt(r.message));
						frm.set_df_property(
							"exchange_rate",
							"description",
							"1 " + frm.doc.currency + " = [?] " + base_currency
						);
					}
				},
			});
		}
		frm.trigger("set_dynamic_field_label");
	},

	exchange_rate: function (frm) {
		$.each(frm.doc.time_logs, function (i, d) {
			calculate_billing_costing_amount(frm, d.doctype, d.name);
		});
		calculate_time_and_amount(frm);
	},

	set_dynamic_field_label: function (frm) {
		let base_currency = nts.defaults.get_global_default("currency");
		frm.set_currency_labels(
			["base_total_costing_amount", "base_total_billable_amount", "base_total_billed_amount"],
			base_currency
		);
		frm.set_currency_labels(
			["total_costing_amount", "total_billable_amount", "total_billed_amount"],
			frm.doc.currency
		);

		frm.toggle_display(
			["base_total_costing_amount", "base_total_billable_amount", "base_total_billed_amount"],
			frm.doc.currency != base_currency
		);

		if (frm.doc.time_logs.length > 0) {
			frm.set_currency_labels(
				["base_billing_rate", "base_billing_amount", "base_costing_rate", "base_costing_amount"],
				base_currency,
				"time_logs"
			);
			frm.set_currency_labels(
				["billing_rate", "billing_amount", "costing_rate", "costing_amount"],
				frm.doc.currency,
				"time_logs"
			);

			let time_logs_grid = frm.fields_dict.time_logs.grid;
			$.each(
				["base_billing_rate", "base_billing_amount", "base_costing_rate", "base_costing_amount"],
				function (i, d) {
					if (nts.meta.get_docfield(time_logs_grid.doctype, d))
						time_logs_grid.set_column_disp(d, frm.doc.currency != base_currency);
				}
			);
		}
		frm.refresh_fields();
	},

	set_route_options_for_new_task: (frm) => {
		let task_field = frm.get_docfield("time_logs", "task");

		if (task_field) {
			task_field.get_route_options_for_new_doc = (row) => ({ project: row.doc.project });
		}
	},

	make_invoice: function (frm) {
		let fields = [
			{
				fieldtype: "Link",
				label: __("Item Code"),
				fieldname: "item_code",
				options: "Item",
			},
		];

		if (!frm.doc.customer) {
			fields.push({
				fieldtype: "Link",
				label: __("Customer"),
				fieldname: "customer",
				options: "Customer",
				default: frm.doc.customer,
			});
		}

		let dialog = new nts.ui.Dialog({
			title: __("Create Sales Invoice"),
			fields: fields,
		});

		dialog.set_primary_action(__("Create Sales Invoice"), () => {
			var args = dialog.get_values();
			if (!args) return;
			dialog.hide();
			return nts.call({
				type: "GET",
				method: "prodman.projects.doctype.timesheet.timesheet.make_sales_invoice",
				args: {
					source_name: frm.doc.name,
					item_code: args.item_code,
					customer: frm.doc.customer || args.customer,
					currency: frm.doc.currency,
				},
				freeze: true,
				callback: function (r) {
					if (!r.exc) {
						nts.model.sync(r.message);
						nts.set_route("Form", r.message.doctype, r.message.name);
					}
				},
			});
		});
		dialog.show();
	},

	parent_project: function (frm) {
		set_project_in_timelog(frm);
	},
});

nts.ui.form.on("Timesheet Detail", {
	time_logs_remove: function (frm) {
		calculate_time_and_amount(frm);
	},

	task: (frm, cdt, cdn) => {
		let row = frm.selected_doc;
		if (row.task) {
			nts.db.get_value("Task", row.task, "project", (r) => {
				nts.model.set_value(cdt, cdn, "project", r.project);
			});
		}
	},

	from_time: function (frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},

	to_time: function (frm, cdt, cdn) {
		var child = locals[cdt][cdn];

		if (frm._setting_hours) return;

		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		nts.model.set_value(cdt, cdn, "hours", hours);
	},

	time_logs_add: function (frm, cdt, cdn) {
		if (frm.doc.parent_project) {
			nts.model.set_value(cdt, cdn, "project", frm.doc.parent_project);
		}
	},

	hours: function (frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
		update_billing_hours(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	billing_hours: function (frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	billing_rate: function (frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	costing_rate: function (frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	is_billable: function (frm, cdt, cdn) {
		update_billing_hours(frm, cdt, cdn);
		update_time_rates(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	activity_type: function (frm, cdt, cdn) {
		if (!nts.get_doc(cdt, cdn).activity_type) return;

		nts.call({
			method: "prodman.projects.doctype.timesheet.timesheet.get_activity_cost",
			args: {
				employee: frm.doc.employee,
				activity_type: frm.selected_doc.activity_type,
				currency: frm.doc.currency,
			},
			callback: function (r) {
				if (r.message) {
					nts.model.set_value(cdt, cdn, "billing_rate", r.message["billing_rate"]);
					nts.model.set_value(cdt, cdn, "costing_rate", r.message["costing_rate"]);
					calculate_billing_costing_amount(frm, cdt, cdn);
				}
			},
		});
	},
});

var calculate_end_time = function (frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if (!child.from_time) {
		// if from_time value is not available then set the current datetime
		nts.model.set_value(cdt, cdn, "from_time", nts.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if (child.hours) {
		d.add(child.hours, "hours");
		frm._setting_hours = true;
		nts.model.set_value(cdt, cdn, "to_time", d.format(nts.defaultDatetimeFormat)).then(() => {
			frm._setting_hours = false;
		});
	}
};

var update_billing_hours = function (frm, cdt, cdn) {
	let child = nts.get_doc(cdt, cdn);
	if (!child.is_billable) {
		nts.model.set_value(cdt, cdn, "billing_hours", 0.0);
	} else {
		// bill all hours by default
		nts.model.set_value(cdt, cdn, "billing_hours", child.hours);
	}
};

var update_time_rates = function (frm, cdt, cdn) {
	let child = nts.get_doc(cdt, cdn);
	if (!child.is_billable) {
		nts.model.set_value(cdt, cdn, "billing_rate", 0.0);
	}
};

var calculate_billing_costing_amount = function (frm, cdt, cdn) {
	let row = nts.get_doc(cdt, cdn);
	let billing_amount = 0.0;
	let base_billing_amount = 0.0;
	let exchange_rate = flt(frm.doc.exchange_rate);
	nts.model.set_value(cdt, cdn, "base_billing_rate", flt(row.billing_rate) * exchange_rate);
	nts.model.set_value(cdt, cdn, "base_costing_rate", flt(row.costing_rate) * exchange_rate);
	if (row.billing_hours && row.is_billable) {
		base_billing_amount = flt(row.billing_hours) * flt(row.base_billing_rate);
		billing_amount = flt(row.billing_hours) * flt(row.billing_rate);
	}

	nts.model.set_value(cdt, cdn, "base_billing_amount", base_billing_amount);
	nts.model.set_value(cdt, cdn, "base_costing_amount", flt(row.base_costing_rate) * flt(row.hours));
	nts.model.set_value(cdt, cdn, "billing_amount", billing_amount);
	nts.model.set_value(cdt, cdn, "costing_amount", flt(row.costing_rate) * flt(row.hours));
};

var calculate_time_and_amount = function (frm) {
	let tl = frm.doc.time_logs || [];
	let total_working_hr = 0;
	let total_billing_hr = 0;
	let total_billable_amount = 0;
	let total_costing_amount = 0;
	for (var i = 0; i < tl.length; i++) {
		if (tl[i].hours) {
			total_working_hr += tl[i].hours;
			total_billable_amount += tl[i].billing_amount;
			total_costing_amount += tl[i].costing_amount;

			if (tl[i].is_billable) {
				total_billing_hr += tl[i].billing_hours;
			}
		}
	}

	frm.set_value("total_billable_hours", total_billing_hr);
	frm.set_value("total_hours", total_working_hr);
	frm.set_value("total_billable_amount", total_billable_amount);
	frm.set_value("total_costing_amount", total_costing_amount);
};

// set employee (and company) to the one that's currently logged in
const set_employee_and_company = function (frm) {
	const options = { user_id: nts.session.user };
	const fields = ["name", "company"];
	nts.db.get_value("Employee", options, fields).then(({ message }) => {
		if (message) {
			// there is an employee with the currently logged in user_id
			frm.set_value("employee", message.name);
			frm.set_value("company", message.company);
		}
	});
};

function set_project_in_timelog(frm) {
	if (frm.doc.parent_project) {
		$.each(frm.doc.time_logs || [], function (i, item) {
			nts.model.set_value(item.doctype, item.name, "project", frm.doc.parent_project);
		});
	}
}
