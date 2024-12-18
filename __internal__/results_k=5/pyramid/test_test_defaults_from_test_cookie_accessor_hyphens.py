import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'session-token': 'abc123'}
        self.helper = DummyCookies(self.request.cookies)

    def test_get_existing_cookie(self):
        result = self.helper.get('session-token')
        self.assertEqual(result, 'abc123')

    def test_get_non_existing_cookie(self):
        result = self.helper.get('non-existing-token')
        self.assertIsNone(result)

    def test_get_cookie_with_hyphen(self):
        self.request.cookies = {'session-token': 'xyz789'}
        result = self.helper.get('session-token')
        self.assertEqual(result, 'xyz789')

    def test_get_cookie_case_sensitivity(self):
        self.request.cookies = {'Session-Token': 'caseSensitiveValue'}
        result = self.helper.get('session-token')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.helper.get('session-token')
        self.assertIsNone(result)

class DummyCookies:
    def __init__(self, cookies):
        self.cookies = cookies

    def get(self, name):
        return self.cookies.get(name)