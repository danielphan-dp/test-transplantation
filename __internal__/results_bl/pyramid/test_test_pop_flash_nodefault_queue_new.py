import unittest
from pyramid.testing import DummySession

class TestSessionGetMethod(unittest.TestCase):

    def setUp(self):
        self.session = DummySession()

    def test_get_cookie_when_set(self):
        self.session.cookie = 'test_cookie'
        result = self.session.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_cookie_when_not_set(self):
        result = self.session.get('cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_different_name(self):
        self.session.cookie = 'another_cookie'
        result = self.session.get('different_name')
        self.assertIsNone(result)

    def test_get_cookie_with_empty_string(self):
        self.session.cookie = ''
        result = self.session.get('cookie')
        self.assertEqual(result, '')

    def test_get_cookie_with_none(self):
        self.session.cookie = None
        result = self.session.get('cookie')
        self.assertIsNone(result)