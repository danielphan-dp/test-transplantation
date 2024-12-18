import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = self._makeRegistry([DummyFactory, None, DummyFactory])
        self.manager = manager

    def test_get_cookie(self):
        request = DummyRequest(cookie={'test_cookie': 'test_value'})
        result = self.manager.get(request)
        self.assertEqual(result.get('test_cookie'), 'test_value')

    def test_get_nonexistent_cookie(self):
        request = DummyRequest(cookie={})
        result = self.manager.get(request)
        self.assertIsNone(result.get('nonexistent_cookie'))

    def test_get_with_multiple_cookies(self):
        request = DummyRequest(cookie={'cookie_one': 'value_one', 'cookie_two': 'value_two'})
        result = self.manager.get(request)
        self.assertEqual(result.get('cookie_one'), 'value_one')
        self.assertEqual(result.get('cookie_two'), 'value_two')

    def test_get_empty_request(self):
        request = DummyRequest(cookie={})
        result = self.manager.get(request)
        self.assertEqual(result, {})

    def test_get_with_invalid_request(self):
        with self.assertRaises(ConfigurationError):
            self.manager.get(None)

    def _makeRegistry(self, factories):
        # Mock implementation of registry creation
        return {'factories': factories}

class DummyRequest:
    def __init__(self, cookie):
        self.cookies = cookie

class DummyFactory:
    pass

if __name__ == '__main__':
    unittest.main()