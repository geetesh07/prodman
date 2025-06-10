# Copyright (c) 2023, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase


class TestSubcontractingBOM(ntsTestCase):
	pass


def create_subcontracting_bom(**kwargs):
	kwargs = nts._dict(kwargs)

	doc = nts.new_doc("Subcontracting BOM")
	doc.is_active = kwargs.is_active or 1
	doc.finished_good = kwargs.finished_good
	doc.finished_good_uom = kwargs.finished_good_uom
	doc.finished_good_qty = kwargs.finished_good_qty or 1
	doc.finished_good_bom = kwargs.finished_good_bom
	doc.service_item = kwargs.service_item
	doc.service_item_uom = kwargs.service_item_uom
	doc.service_item_qty = kwargs.service_item_qty or 1
	doc.save()

	return doc
