import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestYourClass(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with actual initialization if needed

    def test_get_cookie(self):
        self.instance.cookie = 'test_cookie'
        result = self.instance.get('test_name')
        self.assertEqual(result, 'test_cookie')

    def test_get_cookie_empty(self):
        self.instance.cookie = ''
        result = self.instance.get('test_name')
        self.assertEqual(result, '')

    def test_get_cookie_none(self):
        self.instance.cookie = None
        result = self.instance.get('test_name')
        self.assertIsNone(result)

    def test_get_cookie_after_modification(self):
        self.instance.cookie = 'initial_cookie'
        self.instance.cookie = 'modified_cookie'
        result = self.instance.get('test_name')
        self.assertEqual(result, 'modified_cookie')

    def test_get_cookie_with_different_name(self):
        self.instance.cookie = 'another_cookie'
        result = self.instance.get('different_name')
        self.assertEqual(result, 'another_cookie')

if __name__ == '__main__':
    unittest.main()