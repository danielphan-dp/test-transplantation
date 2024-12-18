import unittest
from pyramid.registry import Registry

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.cookie_name = 'test_cookie'
        self.cookie_value = 'cookie_value'
        self.registry.cookies = {self.cookie_name: self.cookie_value}

    def test_get_existing_cookie(self):
        result = self.registry.cookies.get(self.cookie_name)
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self.registry.cookies.get('non_existing_cookie', 'fallback')
        self.assertEqual(result, 'fallback')

    def test_get_cookie_with_fallback(self):
        result = self.registry.cookies.get('another_non_existing_cookie', 'fallback_value')
        self.assertEqual(result, 'fallback_value')

    def test_get_cookie_with_empty_name(self):
        result = self.registry.cookies.get('')
        self.assertIsNone(result)

    def test_get_cookie_with_none_name(self):
        result = self.registry.cookies.get(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()