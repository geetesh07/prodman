import nts 
from nts .tests.utils import nts TestCase

from prodman.accounts.party import get_default_price_list


class PartyTestCase(nts TestCase):
	def test_get_default_price_list_should_return_none_for_invalid_group(self):
		customer = nts .get_doc(
			{
				"doctype": "Customer",
				"customer_name": "test customer",
			}
		).insert(ignore_permissions=True, ignore_mandatory=True)
		customer.customer_group = None
		customer.save()
		price_list = get_default_price_list(customer)
		assert price_list is None
