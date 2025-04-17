import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.policy = self._makeOne()

    def _makeOne(self):
        return DummyCookieHelper('test_cookie_value')

    def test_get_existing_cookie(self):
        result = self.policy.get('test_cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.policy.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.policy = self._makeOne('')
        result = self.policy.get('empty_cookie')
        self.assertEqual(result, '')

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie if name == 'test_cookie' else None

class DummyRequest:
    def __init__(self, environ=None, session=None, registry=None, cookie=None):
        self.environ = environ or {}
        self.session = session or {}
        self.registry = registry
        self.cookies = DummyCookies(cookie)