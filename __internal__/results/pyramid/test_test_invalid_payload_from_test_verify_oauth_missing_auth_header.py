import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b'username:password').decode('ascii')
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials.username, 'username')
        self.assertEqual(credentials.password, 'password')

    def test_missing_authorization_header(self):
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNone(credentials)

    def test_invalid_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNone(credentials)

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNone(credentials)

    def test_no_colon_in_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b'usernamepassword').decode('ascii')
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNone(credentials)

    def test_empty_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b':').decode('ascii')
        credentials = extract_http_basic_credentials(self.request)
        self.assertEqual(credentials.username, '')
        self.assertEqual(credentials.password, '')

if __name__ == '__main__':
    unittest.main()