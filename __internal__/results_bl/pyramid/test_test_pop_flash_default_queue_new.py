import unittest
from pyramid.testing import DummySession

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.session = DummySession()

    def test_get_existing_cookie(self):
        self.session.cookie = 'test_cookie'
        result = self.session.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_non_existing_cookie(self):
        result = self.session.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.session.cookie = None
        result = self.session.get('cookie')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.session.cookie = 'another_cookie'
        result = self.session.get('different_name')
        self.assertEqual(result, 'another_cookie')