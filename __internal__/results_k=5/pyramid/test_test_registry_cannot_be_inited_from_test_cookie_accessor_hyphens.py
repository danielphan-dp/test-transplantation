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
        empty_request = DummyRequest()
        empty_request.cookies = {}
        empty_cookie_helper = DummyCookies(empty_request.cookies)
        result = empty_cookie_helper.get("session-token")
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {"session-token": "abc-123!@#"}
        result = self.cookie_helper.get("session-token")
        self.assertEqual(result, "abc-123!@#")

    def test_registry_cannot_be_inited(self):
        from pyramid.threadlocal import manager

        registry = DummyRegistry()

        def raiseit(name):
            raise TypeError

        registry.__init__ = raiseit
        old = {'registry': registry}
        try:
            manager.push(old)
            self.cookie_helper.get("session-token")  # doesn't blow up
            current = manager.get()
            self.assertNotEqual(current, old)
            self.assertEqual(registry.inited, 1)
        finally:
            manager.clear()