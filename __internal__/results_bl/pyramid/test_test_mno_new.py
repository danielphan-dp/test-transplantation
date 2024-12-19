import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = 'test_cookie'  # Set a default cookie value

    def test_get_existing_cookie(self):
        result = self.instance.get('some_name')
        self.assertEqual(result, 'test_cookie')

    def test_get_no_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('some_name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.instance.cookie = ''
        result = self.instance.get('some_name')
        self.assertEqual(result, '')

    def test_get_with_different_name(self):
        self.instance.cookie = 'another_cookie'
        result = self.instance.get('different_name')
        self.assertEqual(result, 'another_cookie')

    def test_get_with_special_characters(self):
        self.instance.cookie = 'cookie_with_special_chars!@#'
        result = self.instance.get('special_name')
        self.assertEqual(result, 'cookie_with_special_chars!@#')

if __name__ == '__main__':
    unittest.main()