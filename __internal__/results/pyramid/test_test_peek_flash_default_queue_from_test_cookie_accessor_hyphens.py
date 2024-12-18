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

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'session-token': 'abc123'}
        result = self.request.cookies.get('session-token')
        self.assertEqual(result, 'abc123')

    def test_get_cookie_with_empty_name(self):
        result = self.request.cookies.get('')
        self.assertIsNone(result)

    def test_get_cookie_case_sensitivity(self):
        self.request.cookies = {'Test-Cookie': 'value1', 'test-cookie': 'value2'}
        result = self.request.cookies.get('Test-Cookie')
        self.assertEqual(result, 'value1')
        result = self.request.cookies.get('test-cookie')
        self.assertEqual(result, 'value2')