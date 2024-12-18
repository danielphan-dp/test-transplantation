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
        self.request.cookies['special-cookie!'] = 'value@123'
        result = self.request.cookies.get('special-cookie!')
        self.assertEqual(result, 'value@123')

    def test_get_cookie_case_sensitivity(self):
        self.request.cookies['Case-Sensitive-Cookie'] = 'caseValue'
        result = self.request.cookies.get('case-sensitive-cookie')
        self.assertIsNone(result)

    def test_get_cookie_empty_name(self):
        result = self.request.cookies.get('')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()