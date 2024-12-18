import unittest
from pyramid import testing

class TestCookieHelper(unittest.TestCase):

    def _makeOne(self, cookie_value):
        class DummyCookies:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie_value)

    def test_get_cookie(self):
        cookie_value = 'test_cookie_value'
        request = self._makeOne(cookie_value)
        result = request.cookies.get('test_cookie')
        self.assertEqual(result, None)

    def test_get_existing_cookie(self):
        cookie_value = 'test_cookie_value'
        request = self._makeOne(cookie_value)
        request.cookies.cookie = {'test_cookie': cookie_value}
        result = request.cookies.get('test_cookie')
        self.assertEqual(result, cookie_value)

    def test_get_non_existent_cookie(self):
        request = self._makeOne(None)
        result = request.cookies.get('non_existent_cookie')
        self.assertEqual(result, None)

    def test_get_empty_cookie(self):
        request = self._makeOne('')
        result = request.cookies.get('empty_cookie')
        self.assertEqual(result, None)