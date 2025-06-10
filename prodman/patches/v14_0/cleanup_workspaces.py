import nts


def execute():
	for ws in ["Retail", "Utilities"]:
		nts.delete_doc_if_exists("Workspace", ws)

	for ws in ["Integrations", "Settings"]:
		nts.db.set_value("Workspace", ws, "public", 0)
