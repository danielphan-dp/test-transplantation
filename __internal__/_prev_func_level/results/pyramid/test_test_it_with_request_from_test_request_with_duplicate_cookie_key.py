import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_cookie_value(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_with_request(self):
        self._callFUT(request=self.request)
        current = manager.get()
        self.assertEqual(current['request'], self.request)

    def _callFUT(self, request):
        return request.cookies.get('test_cookie')