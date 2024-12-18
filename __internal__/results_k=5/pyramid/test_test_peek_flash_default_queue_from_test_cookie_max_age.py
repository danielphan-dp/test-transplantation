import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {"test_cookie": "test_value"}
        self.session = self._makeOne()

    def _makeOne(self):
        class DummySession:
            def get(self, name):
                return self.request.cookies.get(name)
        return DummySession()

    def test_get_existing_cookie(self):
        result = self.session.get("test_cookie")
        self.assertEqual(result, "test_value")

    def test_get_non_existing_cookie(self):
        result = self.session.get("non_existing_cookie")
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.session.get("empty_cookie")
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {"special_cookie": "value_with_special_characters_!@#$%^&*()"}
        result = self.session.get("special_cookie")
        self.assertEqual(result, "value_with_special_characters_!@#$%^&*()")