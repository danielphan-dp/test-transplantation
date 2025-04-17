import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def _makeOne(self, cookie):
        class DummyCookies:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie)

    def test_get_existing_cookie(self):
        request = self._makeOne('test_cookie_value')
        result = request.cookies.get('test_cookie_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        request = self._makeOne(None)
        result = request.cookies.get('test_cookie_name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        request = self._makeOne('')
        result = request.cookies.get('test_cookie_name')
        self.assertEqual(result, '')