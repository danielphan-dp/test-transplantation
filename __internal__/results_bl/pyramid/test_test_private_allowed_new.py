import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.request = DummyRequest()

    def test_get_with_valid_name(self):
        self.instance.cookie = 'cookie_value'
        result = self.instance.get('valid_name')
        self.assertEqual(result, 'cookie_value')

    def test_get_with_empty_name(self):
        self.instance.cookie = 'cookie_value'
        result = self.instance.get('')
        self.assertEqual(result, 'cookie_value')

    def test_get_with_none_name(self):
        self.instance.cookie = 'cookie_value'
        result = self.instance.get(None)
        self.assertEqual(result, 'cookie_value')

    def test_get_with_unset_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('any_name')
        self.assertIsNone(result)

    def test_get_with_different_cookie_value(self):
        self.instance.cookie = 'another_cookie_value'
        result = self.instance.get('any_name')
        self.assertEqual(result, 'another_cookie_value')

if __name__ == '__main__':
    unittest.main()