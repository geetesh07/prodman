import nts

from prodman.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from prodman.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	get_allowed_types_from_settings,
)


def execute():
	for dt in get_allowed_types_from_settings():
		for dimension in get_accounting_dimensions():
			nts.db.set_value("Custom Field", dt + "-" + dimension, "allow_on_submit", 1)
