import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.cookie_value = 'test_cookie_value'
        self.dummy_request = self._makeRequest(self.cookie_value)
        self.helper = self._makeOne()

    def _makeRequest(self, cookie):
        class DummyCookies:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie if name == 'test_cookie' else None

        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie)

    def _makeOne(self):
        class DummyHelper:
            def get(self, name):
                return self.cookie

        return DummyHelper()

    def test_get_cookie_value(self):
        result = self.helper.get('test_cookie')
        self.assertEqual(result, self.cookie_value)

    def test_get_nonexistent_cookie(self):
        result = self.helper.get('nonexistent_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        empty_request = self._makeRequest('')
        empty_helper = self._makeOne()
        result = empty_helper.get('test_cookie')
        self.assertEqual(result, '')