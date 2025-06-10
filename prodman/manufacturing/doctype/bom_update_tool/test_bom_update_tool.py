# Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import nts
from nts.tests.utils import ntsTestCase, timeout

from prodman.manufacturing.doctype.bom_update_log.test_bom_update_log import (
	update_cost_in_all_boms_in_test,
)
from prodman.manufacturing.doctype.bom_update_tool.bom_update_tool import enqueue_replace_bom
from prodman.manufacturing.doctype.production_plan.test_production_plan import make_bom
from prodman.stock.doctype.item.test_item import create_item

test_records = nts.get_test_records("BOM")


class TestBOMUpdateTool(ntsTestCase):
	"Test major functions run via BOM Update Tool."

	def tearDown(self):
		nts.db.rollback()

	@timeout
	def test_replace_bom(self):
		current_bom = "BOM-_Test Item Home Desktop Manufactured-001"

		bom_doc = nts.copy_doc(test_records[0])
		bom_doc.items[1].item_code = "_Test Item"
		bom_doc.insert()

		boms = nts._dict(current_bom=current_bom, new_bom=bom_doc.name)
		enqueue_replace_bom(boms=boms)

		self.assertFalse(nts.db.exists("BOM Item", {"bom_no": current_bom, "docstatus": 1}))
		self.assertTrue(nts.db.exists("BOM Item", {"bom_no": bom_doc.name, "docstatus": 1}))

	@timeout
	def test_bom_cost(self):
		for item in ["BOM Cost Test Item 1", "BOM Cost Test Item 2", "BOM Cost Test Item 3"]:
			item_doc = create_item(item, valuation_rate=100)
			if item_doc.valuation_rate != 100.00:
				nts.db.set_value("Item", item_doc.name, "valuation_rate", 100)

		bom_no = nts.db.get_value("BOM", {"item": "BOM Cost Test Item 1"}, "name")
		if not bom_no:
			doc = make_bom(
				item="BOM Cost Test Item 1",
				raw_materials=["BOM Cost Test Item 2", "BOM Cost Test Item 3"],
				currency="INR",
			)
		else:
			doc = nts.get_doc("BOM", bom_no)

		self.assertEqual(doc.total_cost, 200)

		nts.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 200)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 300)

		nts.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 100)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 200)
