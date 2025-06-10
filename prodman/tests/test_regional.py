import unittest

import nts

import prodman


@prodman.allow_regional
def test_method():
	return "original"


class TestInit(unittest.TestCase):
	def test_regional_overrides(self):
		nts.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")
