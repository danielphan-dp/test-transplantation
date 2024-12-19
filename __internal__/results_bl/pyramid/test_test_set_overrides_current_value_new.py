import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookie = 'test_cookie'

    def test_get_returns_cookie_value(self):
        result = self.request.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_with_nonexistent_name(self):
        result = self.request.get('nonexistent')
        self.assertEqual(result, None)

    def test_get_with_empty_name(self):
        result = self.request.get('')
        self.assertEqual(result, None)

    def test_get_after_modifying_cookie(self):
        self.request.cookie = 'modified_cookie'
        result = self.request.get('cookie')
        self.assertEqual(result, 'modified_cookie')