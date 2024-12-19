import unittest
from pyramid.testing import DummyRequest, DummyResponse

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.view = AView()

    def test_get_method_returns_cookie(self):
        self.view.cookie = 'test_cookie'
        result = self.view.get('test_name')
        self.assertEqual(result, 'test_cookie')

    def test_get_method_with_no_cookie(self):
        self.view.cookie = None
        result = self.view.get('test_name')
        self.assertIsNone(result)

    def test_get_method_with_empty_string_cookie(self):
        self.view.cookie = ''
        result = self.view.get('test_name')
        self.assertEqual(result, '')

    def test_get_method_with_non_string_cookie(self):
        self.view.cookie = 12345
        result = self.view.get('test_name')
        self.assertEqual(result, 12345)

class AView:
    def __init__(self):
        self.response = DummyResponse()
        self.cookie = None

    def get(self, name):
        return self.cookie