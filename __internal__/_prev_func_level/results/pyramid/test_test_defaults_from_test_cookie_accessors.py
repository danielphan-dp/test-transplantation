import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_cookie_exists(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_cookie_not_exists(self):
        result = self.request.cookies.get('non_existent_cookie', 'fallback_value')
        self.assertEqual(result, 'fallback_value')

    def test_get_cookie_with_default(self):
        result = self.request.cookies.get('another_cookie', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_get_cookie_with_empty_string(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_cookie_with_none(self):
        self.request.cookies['none_cookie'] = None
        result = self.request.cookies.get('none_cookie')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()