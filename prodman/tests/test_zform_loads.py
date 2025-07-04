""" smoak tests to check basic functionality calls on known form loads."""

import nts
from nts.desk.form.load import getdoc
from nts.tests.utils import ntsTestCase, change_settings
from nts.www.printview import get_html_and_style


class TestFormLoads(ntsTestCase):
	@change_settings("Print Settings", {"allow_print_for_cancelled": 1})
	def test_load(self):
		prodman_modules = nts.get_all("Module Def", filters={"app_name": "prodman"}, pluck="name")
		doctypes = nts.get_all(
			"DocType",
			{"istable": 0, "issingle": 0, "is_virtual": 0, "module": ("in", prodman_modules)},
			pluck="name",
		)

		for doctype in doctypes:
			last_doc = nts.db.get_value(doctype, {}, "name", order_by="modified desc")
			if not last_doc:
				continue
			with self.subTest(msg=f"Loading {doctype} - {last_doc}", doctype=doctype, last_doc=last_doc):
				self.assertFormLoad(doctype, last_doc)
				self.assertDocPrint(doctype, last_doc)

	def assertFormLoad(self, doctype, docname):
		# reset previous response
		nts.response = nts._dict({"docs": []})
		nts.response.docinfo = None

		try:
			getdoc(doctype, docname)
		except Exception as e:
			self.fail(f"Failed to load {doctype}-{docname}: {e}")

		self.assertTrue(
			nts.response.docs, msg=f"expected document in reponse, found: {nts.response.docs}"
		)
		self.assertTrue(
			nts.response.docinfo, msg=f"expected docinfo in reponse, found: {nts.response.docinfo}"
		)

	def assertDocPrint(self, doctype, docname):
		doc = nts.get_doc(doctype, docname)
		doc.set("__onload", nts._dict())
		doc.run_method("onload")

		messages_before = nts.get_message_log()
		ret = get_html_and_style(doc=doc.as_json(), print_format="Standard", no_letterhead=1)
		messages_after = nts.get_message_log()

		if len(messages_after) > len(messages_before):
			new_messages = messages_after[len(messages_before) :]
			self.fail("Print view showing error/warnings: \n" + "\n".join(str(msg) for msg in new_messages))

		# html should exist
		self.assertTrue(bool(ret["html"]))
