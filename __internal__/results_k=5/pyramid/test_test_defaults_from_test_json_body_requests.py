import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'cookie_value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get('any_cookie')
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        self.request.cookies = {'special_cookie!@#': 'special_value'}
        result = self.request.cookies.get('special_cookie!@#')
        self.assertEqual(result, 'special_value')

    def test_get_cookie_case_sensitivity(self):
        self.request.cookies = {'Test_Cookie': 'value1', 'test_cookie': 'value2'}
        result = self.request.cookies.get('Test_Cookie')
        self.assertEqual(result, 'value1')
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'value2')