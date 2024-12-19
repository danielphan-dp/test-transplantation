import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestYourClass(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()
        self.instance.cookie = 'test_cookie_value'

    def test_get_existing_cookie(self):
        result = self.instance.get('test_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('test_name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.instance.cookie = ''
        result = self.instance.get('test_name')
        self.assertEqual(result, '')

    def test_get_with_special_characters(self):
        self.instance.cookie = 'cookie_with_special_chars_!@#$%^&*()'
        result = self.instance.get('test_name')
        self.assertEqual(result, 'cookie_with_special_chars_!@#$%^&*()')

if __name__ == '__main__':
    unittest.main()