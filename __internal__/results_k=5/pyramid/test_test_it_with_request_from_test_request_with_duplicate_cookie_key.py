import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_cookie_value(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_with_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get('any_cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'special_cookie': 'value_with_special_chars_!@#$%^&*()'}
        result = self.request.cookies.get('special_cookie')
        self.assertEqual(result, 'value_with_special_chars_!@#$%^&*()')

    def test_get_cookie_case_sensitivity(self):
        self.request.cookies = {'CaseSensitiveCookie': 'value'}
        result = self.request.cookies.get('casesensitivecookie')
        self.assertIsNone(result)

    def test_get_cookie_after_modification(self):
        self.request.cookies['modifiable_cookie'] = 'initial_value'
        self.request.cookies['modifiable_cookie'] = 'modified_value'
        result = self.request.cookies.get('modifiable_cookie')
        self.assertEqual(result, 'modified_value')

    def test_get_cookie_with_duplicate_keys(self):
        self.request.cookies = {'duplicate_cookie': 'value1,value2'}
        result = self.request.cookies.get('duplicate_cookie')
        self.assertEqual(result, 'value1,value2')

    def test_get_cookie_with_none_value(self):
        self.request.cookies = {'none_value_cookie': None}
        result = self.request.cookies.get('none_value_cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_numeric_key(self):
        self.request.cookies = {123: 'numeric_key_value'}
        result = self.request.cookies.get(123)
        self.assertEqual(result, 'numeric_key_value')

    def test_get_cookie_with_boolean_key(self):
        self.request.cookies = {True: 'boolean_key_value'}
        result = self.request.cookies.get(True)
        self.assertEqual(result, 'boolean_key_value')