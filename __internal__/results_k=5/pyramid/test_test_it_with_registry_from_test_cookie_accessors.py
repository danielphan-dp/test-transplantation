import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}
        self._callFUT = self.get_method

    def get_method(self, request):
        return request.cookies.get('test_cookie', None)

    def test_get_cookie_value(self):
        result = self._callFUT(self.request)
        self.assertEqual(result, 'test_value')

    def test_get_non_existent_cookie(self):
        self.request.cookies = {}
        result = self._callFUT(self.request)
        self.assertIsNone(result)

    def test_get_cookie_with_fallback(self):
        result = self._callFUT(self.request)
        self.assertEqual(result, 'test_value')

    def test_it_with_registry(self):
        self._callFUT(self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

if __name__ == '__main__':
    unittest.main()