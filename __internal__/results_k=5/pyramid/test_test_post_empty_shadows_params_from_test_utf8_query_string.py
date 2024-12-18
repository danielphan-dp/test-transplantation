import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.cookie_value = 'test_cookie_value'
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': self.cookie_value}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        special_cookie_value = 'cookie_with_special_chars!@#$%^&*()'
        self.request.cookies['special_cookie'] = special_cookie_value
        result = self.request.cookies.get('special_cookie')
        self.assertEqual(result, special_cookie_value)