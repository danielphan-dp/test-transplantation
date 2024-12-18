import unittest
from pyramid.registry import Registry

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.cookie_name = 'test_cookie'
        self.cookie_value = 'test_value'
        self.registry.cookies = {self.cookie_name: self.cookie_value}

    def test_get_existing_cookie(self):
        result = self.registry.cookies.get(self.cookie_name)
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self.registry.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_with_duplicate_cookie_key(self):
        self.registry.cookies[self.cookie_name] = 'value_one; value_two'
        result = self.registry.cookies.get(self.cookie_name)
        self.assertEqual(result, 'value_one; value_two')

    def test_get_empty_cookie(self):
        self.registry.cookies[self.cookie_name] = ''
        result = self.registry.cookies.get(self.cookie_name)
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        special_cookie_name = 'special_cookie'
        special_cookie_value = 'value_with_special_chars!@#$%^&*()'
        self.registry.cookies[special_cookie_name] = special_cookie_value
        result = self.registry.cookies.get(special_cookie_name)
        self.assertEqual(result, special_cookie_value)