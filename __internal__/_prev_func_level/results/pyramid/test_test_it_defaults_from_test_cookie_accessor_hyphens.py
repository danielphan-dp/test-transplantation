import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import get_current_registry, manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test-cookie': 'test-value'}
        self.registry = Registry()
        self.registry.settings = {}
        self.request.registry = self.registry

    def test_get_cookie(self):
        cookie_value = self.request.cookies.get('test-cookie')
        self.assertEqual(cookie_value, 'test-value')

    def test_get_non_existent_cookie(self):
        cookie_value = self.request.cookies.get('non-existent-cookie')
        self.assertIsNone(cookie_value)

    def test_get_with_empty_cookie(self):
        self.request.cookies = {}
        cookie_value = self.request.cookies.get('test-cookie')
        self.assertIsNone(cookie_value)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'session-token': 'abc123'}
        cookie_value = self.request.cookies.get('session-token')
        self.assertEqual(cookie_value, 'abc123')

    def test_get_cookie_with_hyphen(self):
        self.request.cookies = {'session-token': 'abc123'}
        cookie_value = self.request.cookies.get('session-token')
        self.assertEqual(cookie_value, 'abc123')

if __name__ == '__main__':
    unittest.main()