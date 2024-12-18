import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test-cookie': 'test-value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test-cookie')
        self.assertEqual(result, 'test-value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non-existing-cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies['empty-cookie'] = ''
        result = self.request.cookies.get('empty-cookie')
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        self.request.cookies['special-cookie'] = 'value@123'
        result = self.request.cookies.get('special-cookie')
        self.assertEqual(result, 'value@123')