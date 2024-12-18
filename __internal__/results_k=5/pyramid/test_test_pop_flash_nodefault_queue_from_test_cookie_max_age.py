import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {"test": "cookie_value"}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get("test")
        self.assertEqual(result, "cookie_value")

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get("non_existing")
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get("test")
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {"test!@#": "value_with_special_chars"}
        result = self.request.cookies.get("test!@#")
        self.assertEqual(result, "value_with_special_chars")