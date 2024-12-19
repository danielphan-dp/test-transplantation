import unittest
from pyramid.request import Request
from pyramid.response import Response

class TestGetMethod(unittest.TestCase):
    
    def setUp(self):
        self.request = Request({})
        self.request.cookies = {'test_cookie': 'cookie_value'}
    
    def test_get_existing_cookie(self):
        result = self.request.get('test_cookie')
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.request.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.get('empty_cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'special_cookie!@#': 'special_value'}
        result = self.request.get('special_cookie!@#')
        self.assertEqual(result, 'special_value')