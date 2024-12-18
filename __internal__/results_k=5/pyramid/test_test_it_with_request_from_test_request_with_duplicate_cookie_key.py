import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'foo': 'one', 'bar': 'two'}

    def test_get_cookie_value(self):
        result = self.request.cookies.get('foo')
        self.assertEqual(result, 'one')

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get('baz')
        self.assertIsNone(result)

    def test_get_multiple_cookies(self):
        self.request.cookies['foo'] = 'one; two'
        result = self.request.cookies.getlist('foo')
        self.assertEqual(result, ['one', 'two'])

    def test_get_cookie_with_empty_value(self):
        self.request.cookies['empty'] = ''
        result = self.request.cookies.get('empty')
        self.assertEqual(result, '')

    def test_it_with_request(self):
        self._callFUT(request=self.request)
        current = manager.get()
        self.assertEqual(current['request'], self.request)

    def _callFUT(self, request):
        return request.cookies