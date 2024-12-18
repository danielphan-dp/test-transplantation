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
        result = self.request.cookies.get('non_existing_cookie', 'fallback_value')
        self.assertEqual(result, 'fallback_value')

    def test_get_empty_cookie(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_with_default_value(self):
        result = self.request.cookies.get('another_non_existing_cookie', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_get_multiple_cookies(self):
        self.request.cookies.update({'cookie_one': 'value_one', 'cookie_two': 'value_two'})
        result_one = self.request.cookies.get('cookie_one')
        result_two = self.request.cookies.get('cookie_two')
        self.assertEqual(result_one, 'value_one')
        self.assertEqual(result_two, 'value_two')

if __name__ == '__main__':
    unittest.main()