import click
import nts


def execute():
	if "webshop" in nts.get_installed_apps():
		return

	if not nts.db.table_exists("Website Item"):
		return

	doctypes = [
		"E Commerce Settings",
		"Website Item",
		"Recommended Items",
		"Item Review",
		"Wishlist Item",
		"Wishlist",
		"Website Offer",
		"Website Item Tabbed Section",
	]

	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"ECommerce is renamed and moved to a separate app"
		"Please install the app for ECommerce features: https://github.com/nts/webshop",
		fg="yellow",
	)
