import nts


def execute():
	for doctype in ["Customer", "Supplier"]:
		field = doctype.lower() + "_type"
		nts.db.set_value(doctype, {field: "Proprietorship"}, field, "Individual")
