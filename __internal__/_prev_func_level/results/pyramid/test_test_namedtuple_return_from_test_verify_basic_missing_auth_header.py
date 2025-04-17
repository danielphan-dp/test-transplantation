import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_basic_auth(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr:pass', 'utf-8')
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result.username, 'chrisr')
        self.assertEqual(result.password, 'pass')

    def test_missing_auth_header(self):
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Bearer token'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_no_username_password(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes(':', 'utf-8')
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_only_username(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr:', 'utf-8')
        ).decode('ascii')
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()