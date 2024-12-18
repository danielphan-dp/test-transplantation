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
                return self.cookie

        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie)

    def _makeOne(self):
        class DummyHelper:
            def get(self, name):
                return self.cookie

            @property
            def cookie(self):
                return self.cookie_value

        return DummyHelper()

    def test_get_existing_cookie(self):
        result = self.helper.get('test_cookie')
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self.helper.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.helper.cookie_value = ''
        result = self.helper.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        self.helper.cookie_value = 'cookie_with_special_!@#$%^&*()'
        result = self.helper.get('special_cookie')
        self.assertEqual(result, 'cookie_with_special_!@#$%^&*()')