import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_basic_auth_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b'chrisr:pass'
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result.username, 'chrisr')
        self.assertEqual(result.password, 'pass')

    def test_missing_authorization_header(self):
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_malformed_authorization_header(self):
        self.request.headers['Authorization'] = 'Basic'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_no_username_password(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b':'
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result.username, '')
        self.assertEqual(result.password, '')

    def test_only_username(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b'username:'
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result.username, 'username')
        self.assertEqual(result.password, '')

    def test_only_password(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b':password'
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result.username, '')
        self.assertEqual(result.password, 'password')

if __name__ == '__main__':
    unittest.main()