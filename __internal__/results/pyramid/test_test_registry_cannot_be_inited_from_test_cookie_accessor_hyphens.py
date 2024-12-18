import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {"session-token": "abc123"}
        self.cookie_helper = DummyCookies(self.request.cookies)

    def test_get_existing_cookie(self):
        result = self.cookie_helper.get("session-token")
        self.assertEqual(result, "abc123")

    def test_get_non_existing_cookie(self):
        result = self.cookie_helper.get("non-existing-token")
        self.assertIsNone(result)

    def test_get_with_empty_cookie(self):
        empty_cookie_helper = DummyCookies({})
        result = empty_cookie_helper.get("session-token")
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        self.request.cookies = {"session-token!@#": "abc123"}
        result = self.cookie_helper.get("session-token!@#")
        self.assertEqual(result, "abc123")

    def test_get_with_hyphen_in_name(self):
        self.request.cookies = {"session-token": "abc123"}
        result = self.cookie_helper.get("session-token")
        self.assertEqual(result, "abc123")

    def tearDown(self):
        manager.clear()