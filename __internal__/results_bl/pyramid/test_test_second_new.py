import unittest
from pyramid.request import Request
from pyramid.response import Response

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = Request({})
        self.request.cookie = 'test_cookie_value'
    
    def test_get_method_returns_cookie(self):
        result = self.request.get('cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_no_cookie(self):
        self.request.cookie = None
        result = self.request.get('cookie')
        self.assertIsNone(result)

    def test_get_method_with_empty_cookie(self):
        self.request.cookie = ''
        result = self.request.get('cookie')
        self.assertEqual(result, '')