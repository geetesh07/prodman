import os

import nts
from nts import _


def execute():
	nts.reload_doc("email", "doctype", "email_template")
	nts.reload_doc("stock", "doctype", "delivery_settings")

	if not nts.db.exists("Email Template", _("Dispatch Notification")):
		base_path = nts.get_app_path("prodman", "stock", "doctype")
		response = nts.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		nts.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": nts.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = nts.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
