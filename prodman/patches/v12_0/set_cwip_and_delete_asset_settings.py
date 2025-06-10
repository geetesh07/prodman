import nts
from nts.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if nts.db.exists("DocType", "Asset Settings"):
		nts.reload_doctype("Asset Category")
		cwip_value = nts.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		nts.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		nts.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		nts.delete_doc_if_exists("DocType", "Asset Settings")
