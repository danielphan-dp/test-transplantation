import unittest
from pyramid.testing import DummyRequest
from pyramid.session import SignedCookieSessionFactory

class TestSessionMethods(unittest.TestCase):

    def setUp(self):
        self.factory = SignedCookieSessionFactory('secret')
        self.request = DummyRequest()
        self.session = self.factory(self.request)

    def test_get_cookie(self):
        self.session.cookie = 'test_cookie_value'
        result = self.session.get('cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existent_cookie(self):
        result = self.session.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.session.cookie = None
        result = self.session.get('cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_different_name(self):
        self.session.cookie = 'another_cookie_value'
        result = self.session.get('different_cookie_name')
        self.assertEqual(result, 'another_cookie_value')