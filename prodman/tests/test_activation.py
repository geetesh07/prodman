from nts.tests.utils import ntsTestCase

from prodman.utilities.activation import get_level


class TestActivation(ntsTestCase):
	def test_activation(self):
		levels = get_level()
		self.assertTrue(levels)
