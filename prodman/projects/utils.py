# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import nts


@nts.whitelist()
@nts.validate_and_sanitize_search_inputs
def query_task(doctype, txt, searchfield, start, page_len, filters):
	from nts.desk.reportview import build_match_conditions

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_conditions = build_match_conditions("Task")
	match_conditions = ("and" + match_conditions) if match_conditions else ""

	return nts.db.sql(
		"""select name, subject from `tabTask`
		where (`{}` like {} or `subject` like {}) {}
		order by
			case when `subject` like {} then 0 else 1 end,
			case when `{}` like {} then 0 else 1 end,
			`{}`,
			subject
		limit {} offset {}""".format(
			searchfield, "%s", "%s", match_conditions, "%s", searchfield, "%s", searchfield, "%s", "%s"
		),
		(search_string, search_string, order_by_string, order_by_string, page_len, start),
	)
