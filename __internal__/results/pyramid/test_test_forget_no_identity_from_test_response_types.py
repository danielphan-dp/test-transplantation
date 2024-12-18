import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def _makeRequest(self, cookie_value=None):
        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = {'name': cookie}

        return DummyRequest(cookie_value)

    def _makeOne(self):
        class DummyHelper:
            def get(self, name):
                return self.cookies.get(name)

        return DummyHelper()

    def test_get_existing_cookie(self):
        request = self._makeRequest(cookie_value='test_cookie_value')
        helper = self._makeOne()
        result = helper.get('name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        request = self._makeRequest(cookie_value=None)
        helper = self._makeOne()
        result = helper.get('name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        request = self._makeRequest(cookie_value='')
        helper = self._makeOne()
        result = helper.get('name')
        self.assertEqual(result, '')

    def test_get_with_different_cookie_name(self):
        request = self._makeRequest(cookie_value='another_value')
        helper = self._makeOne()
        result = helper.get('different_name')
        self.assertIsNone(result)