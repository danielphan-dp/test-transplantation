import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get('any_cookie')
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        self.request.cookies = {'special_cookie!@#': 'value123'}
        result = self.request.cookies.get('special_cookie!@#')
        self.assertEqual(result, 'value123')

    def test_get_case_sensitive_cookie(self):
        self.request.cookies = {'CaseSensitiveCookie': 'value1', 'casesensitivecookie': 'value2'}
        result = self.request.cookies.get('CaseSensitiveCookie')
        self.assertEqual(result, 'value1')
        result = self.request.cookies.get('casesensitivecookie')
        self.assertEqual(result, 'value2')