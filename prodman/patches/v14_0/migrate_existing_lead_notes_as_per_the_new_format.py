import nts
from nts.utils import cstr, strip_html


def execute():
	for doctype in ("Lead", "Prospect", "Opportunity"):
		if not nts.db.has_column(doctype, "notes"):
			continue

		dt = nts.qb.DocType(doctype)
		records = (
			nts.qb.from_(dt).select(dt.name, dt.notes).where(dt.notes.isnotnull() & dt.notes != "")
		).run(as_dict=True)

		for d in records:
			if strip_html(cstr(d.notes)).strip():
				doc = nts.get_doc(doctype, d.name)
				doc.append("notes", {"note": d.notes})
				doc.update_child_table("notes")

		nts.db.sql_ddl(f"alter table `tab{doctype}` drop column `notes`")
