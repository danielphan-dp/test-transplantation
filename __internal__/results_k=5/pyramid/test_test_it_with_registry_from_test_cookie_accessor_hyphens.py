import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'session-token': 'abc123'}
        self.cookie_helper = self.registry.queryUtility(CookieHelper)

    def test_get_cookie(self):
        result = self.cookie_helper.get('session-token')
        self.assertEqual(result, 'abc123')

    def test_get_non_existent_cookie(self):
        result = self.cookie_helper.get('non-existent-token')
        self.assertIsNone(result)

    def test_get_cookie_with_hyphen(self):
        self.request.cookies = {'session-token': 'xyz789'}
        result = self.cookie_helper.get('session-token')
        self.assertEqual(result, 'xyz789')

    def test_get_cookie_with_empty_name(self):
        with self.assertRaises(KeyError):
            self.cookie_helper.get('')

    def test_get_cookie_with_none(self):
        result = self.cookie_helper.get(None)
        self.assertIsNone(result)

    def test_it_with_registry(self):
        self._callFUT(registry=self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

if __name__ == '__main__':
    unittest.main()