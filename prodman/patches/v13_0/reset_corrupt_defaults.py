import nts


def execute():
	"""
	This patch is needed to fix parent incorrectly set as `__2fa` because of
	https://github.com/nts/nts/commit/a822092211533ff17ff9b92dd86f6f868ed63e2e
	"""

	for doctype in (
		"Accounts Settings",
		"Stock Settings",
		"Selling Settings",
		"Buying Settings",
		"CRM Settings",
		"Global Defaults",
		"Healthcare Settings",
		"Education Settings",
	):
		try:
			nts.get_single(doctype).save()
		except Exception:
			pass

	try:
		pos_profile = nts.get_last_doc("POS Profile")
		pos_profile.set_defaults()
	except Exception:
		pass
