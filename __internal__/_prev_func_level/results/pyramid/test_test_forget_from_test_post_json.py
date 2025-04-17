import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

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

    def test_get_valid_cookie(self):
        request = self._makeOne('valid_cookie_value')
        result = request.cookies.get('cookie_name')
        self.assertEqual(result, 'valid_cookie_value')

    def test_get_none_cookie(self):
        request = self._makeOne(None)
        result = request.cookies.get('cookie_name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        request = self._makeOne('')
        result = request.cookies.get('cookie_name')
        self.assertEqual(result, '')

    def test_get_nonexistent_cookie(self):
        request = self._makeOne('some_cookie_value')
        result = request.cookies.get('nonexistent_cookie')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()