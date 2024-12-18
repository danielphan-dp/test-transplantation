import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}
        self.cookie_helper = self._make_cookie_helper()

    def _make_cookie_helper(self):
        class CookieHelper:
            def get(self, name):
                return self.request.cookies.get(name)
        return CookieHelper()

    def test_get_cookie_value(self):
        result = self.cookie_helper.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existent_cookie(self):
        result = self.cookie_helper.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_with_registry(self):
        self._callFUT(registry=self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

    def _callFUT(self, registry):
        self.registry = registry
        return self.cookie_helper.get('test_cookie')

if __name__ == '__main__':
    unittest.main()