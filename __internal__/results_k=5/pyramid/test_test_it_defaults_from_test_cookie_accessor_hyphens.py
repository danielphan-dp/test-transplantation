import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import get_current_registry, manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.cookie_name = "test-cookie"
        self.cookie_value = "cookie_value"
        self.request.cookies[self.cookie_name] = self.cookie_value

    def test_get_existing_cookie(self):
        result = self.request.cookies.get(self.cookie_name)
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get("non-existing-cookie")
        self.assertIsNone(result)

    def test_get_cookie_with_hyphen(self):
        self.request.cookies["session-token"] = "abc123"
        result = self.request.cookies.get("session-token")
        self.assertEqual(result, "abc123")

    def test_get_cookie_with_special_characters(self):
        self.request.cookies["special@cookie"] = "value!@#"
        result = self.request.cookies.get("special@cookie")
        self.assertEqual(result, "value!@#")

    def test_get_cookie_with_empty_name(self):
        result = self.request.cookies.get("")
        self.assertIsNone(result)

    def test_get_cookie_with_none_name(self):
        result = self.request.cookies.get(None)
        self.assertIsNone(result)

    def test_get_cookie_after_modification(self):
        self.request.cookies[self.cookie_name] = "new_value"
        result = self.request.cookies.get(self.cookie_name)
        self.assertEqual(result, "new_value")

if __name__ == '__main__':
    unittest.main()