import unittest

from tests.sample_sdk_https import SampleHttpsHttpSdk
from sdklib.html import HTML


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleHttpsHttpSdk.set_default_proxy("localhost:8080")
        cls.api = SampleHttpsHttpSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def _test_get_products(self):
        response = self.api.get_products()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.data, list))

    def _test_redirect_true(self):
        response = self.api.checkout(redirect=True)
        self.assertEqual(response.status, 200)

    def _test_redirect_false(self):
        response = self.api.checkout(redirect=False)
        self.assertEqual(response.status, 302)

    def _test_html_response(self):
        response = self.api.home()
        self.assertTrue(isinstance(response.html, HTML))
