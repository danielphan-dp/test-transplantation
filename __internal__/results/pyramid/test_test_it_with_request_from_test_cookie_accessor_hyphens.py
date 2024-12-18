import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test-cookie': 'test-value'}
        self.cookie_helper = DummyCookies(self.request.cookies)

    def test_get_existing_cookie(self):
        result = self.cookie_helper.get('test-cookie')
        self.assertEqual(result, 'test-value')

    def test_get_non_existing_cookie(self):
        result = self.cookie_helper.get('non-existing-cookie')
        self.assertIsNone(result)

    def test_get_with_request(self):
        self._callFUT(request=self.request)
        current = manager.get()
        self.assertEqual(current['request'], self.request)

    def _callFUT(self, request):
        return self.cookie_helper.get(request.cookies.get('test-cookie'))