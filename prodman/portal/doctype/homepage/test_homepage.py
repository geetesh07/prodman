# Copyright (c) 2019, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import nts
from nts.utils import set_request
from nts.website.serve import get_response


class TestHomepage(unittest.TestCase):
	def test_homepage_load(self):
		set_request(method="GET", path="home")
		response = get_response()

		self.assertEqual(response.status_code, 200)

		html = nts.safe_decode(response.get_data())
		self.assertTrue('<section class="hero-section' in html)
