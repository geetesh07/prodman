# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts
from nts import _

from prodman.setup.demo import setup_demo_data
from prodman.setup.setup_wizard.operations import install_fixtures as fixtures


def get_setup_stages(args=None):
	if nts.db.sql("select name from tabCompany"):
		stages = [
			{
				"status": _("Wrapping up"),
				"fail_msg": _("Failed to login"),
				"tasks": [{"fn": fin, "args": args, "fail_msg": _("Failed to login")}],
			}
		]
	else:
		stages = [
			{
				"status": _("Installing presets"),
				"fail_msg": _("Failed to install presets"),
				"tasks": [{"fn": stage_fixtures, "args": args, "fail_msg": _("Failed to install presets")}],
			},
			{
				"status": _("Setting up company"),
				"fail_msg": _("Failed to setup company"),
				"tasks": [{"fn": setup_company, "args": args, "fail_msg": _("Failed to setup company")}],
			},
			{
				"status": _("Setting defaults"),
				"fail_msg": "Failed to set defaults",
				"tasks": [
					{"fn": setup_defaults, "args": args, "fail_msg": _("Failed to setup defaults")},
				],
			},
			{
				"status": _("Wrapping up"),
				"fail_msg": _("Failed to login"),
				"tasks": [{"fn": fin, "args": args, "fail_msg": _("Failed to login")}],
			},
		]

	return stages


def stage_fixtures(args):
	fixtures.install(args.get("country"))


def setup_company(args):
	fixtures.install_company(args)


def setup_defaults(args):
	fixtures.install_defaults(nts._dict(args))


def fin(args):
	nts.local.message_log = []
	login_as_first_user(args)


def setup_demo(args):
	if args.get("setup_demo"):
		nts.enqueue(setup_demo_data, enqueue_after_commit=True, at_front=True)


def login_as_first_user(args):
	if args.get("email") and hasattr(nts.local, "login_manager"):
		nts.local.login_manager.login_as(args.get("email"))


# Only for programmatical use
def setup_complete(args=None):
	stage_fixtures(args)
	setup_company(args)
	setup_defaults(args)
	fin(args)
