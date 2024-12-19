import unittest
from pyramid.testing import DummyRequest
from your_module import YourSessionClass  # Replace with the actual module and class name

class TestSession(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.session = YourSessionClass(self.request)

    def test_get_cookie(self):
        self.session.cookie = 'test_cookie'
        result = self.session.get('cookie_name')
        self.assertEqual(result, 'test_cookie')

    def test_get_non_existent_cookie(self):
        result = self.session.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.session.cookie = None
        result = self.session.get('cookie_name')
        self.assertIsNone(result)

    def test_get_cookie_with_different_name(self):
        self.session.cookie = 'another_cookie'
        result = self.session.get('different_cookie_name')
        self.assertEqual(result, 'another_cookie')