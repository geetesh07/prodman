import click
import nts


def execute():
	if "taxjar_integration" in nts.get_installed_apps():
		return

	doctypes = ["TaxJar Settings", "TaxJar Nexus", "Product Tax Category"]
	for doctype in doctypes:
		nts.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"Taxjar Integration is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/nts/taxjar_integration",
		fg="yellow",
	)
