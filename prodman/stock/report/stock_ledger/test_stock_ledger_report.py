# Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase
from nts.utils import add_days, today

from prodman.maintenance.doctype.maintenance_schedule.test_maintenance_schedule import (
	make_serial_item_with_serial,
)


class TestStockLedgerReeport(ntsTestCase):
	def setUp(self) -> None:
		make_serial_item_with_serial("_Test Stock Report Serial Item")
		self.filters = nts._dict(
			company="_Test Company",
			from_date=today(),
			to_date=add_days(today(), 30),
			item_code="_Test Stock Report Serial Item",
		)

	def tearDown(self) -> None:
		nts.db.rollback()
