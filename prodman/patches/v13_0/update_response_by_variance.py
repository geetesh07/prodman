# Copyright (c) 2020, nts and Contributors
# License: GNU General Public License v3. See license.txt


import nts


def execute():
	if nts.db.exists("DocType", "Issue") and nts.db.count("Issue"):
		invalid_issues = nts.get_all(
			"Issue",
			{"first_responded_on": ["is", "set"], "response_by_variance": ["<", 0]},
			[
				"name",
				"response_by_variance",
				"timestampdiff(Second, `first_responded_on`, `response_by`) as variance",
			],
		)

		# issues which has response_by_variance set as -ve
		# but diff between first_responded_on & response_by is +ve i.e SLA isn't failed
		invalid_issues = [d for d in invalid_issues if d.get("variance") > 0]

		for issue in invalid_issues:
			nts.db.set_value(
				"Issue",
				issue.get("name"),
				"response_by_variance",
				issue.get("variance"),
				update_modified=False,
			)

		invalid_issues = nts.get_all(
			"Issue",
			{"resolution_date": ["is", "set"], "resolution_by_variance": ["<", 0]},
			[
				"name",
				"resolution_by_variance",
				"timestampdiff(Second, `resolution_date`, `resolution_by`) as variance",
			],
		)

		# issues which has resolution_by_variance set as -ve
		# but diff between resolution_date & resolution_by is +ve i.e SLA isn't failed
		invalid_issues = [d for d in invalid_issues if d.get("variance") > 0]

		for issue in invalid_issues:
			nts.db.set_value(
				"Issue",
				issue.get("name"),
				"resolution_by_variance",
				issue.get("variance"),
				update_modified=False,
			)
