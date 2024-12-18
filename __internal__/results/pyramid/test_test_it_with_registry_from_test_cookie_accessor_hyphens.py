import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'session-token': 'abc123'}
        self.cookie_helper = self._make_cookie_helper()

    def _make_cookie_helper(self):
        class CookieHelper:
            def get(self, name):
                return self.request.cookies.get(name)
        return CookieHelper()

    def test_get_cookie(self):
        result = self.cookie_helper.get("session-token")
        self.assertEqual(result, 'abc123')

    def test_get_non_existent_cookie(self):
        result = self.cookie_helper.get("non-existent-token")
        self.assertIsNone(result)

    def test_get_cookie_with_registry(self):
        self._callFUT(registry=self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

    def _callFUT(self, registry):
        manager.set({'registry': registry})