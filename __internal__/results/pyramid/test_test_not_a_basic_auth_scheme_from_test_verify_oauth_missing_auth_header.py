import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_no_auth_header(self):
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Basic'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_non_basic_auth_scheme(self):
        self.request.headers['Authorization'] = 'OtherScheme %s' % base64.b64encode(
            bytes('chrisr:password', 'utf-8')
        ).decode('ascii')
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_valid_basic_auth(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr:password', 'utf-8')
        ).decode('ascii')
        credentials = extract_http_basic_credentials(self.request)
        self.assertEqual(credentials.username, 'chrisr')
        self.assertEqual(credentials.password, 'password')

    def test_invalid_username_password_split(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr', 'utf-8')
        ).decode('ascii')
        self.assertIsNone(extract_http_basic_credentials(self.request))

if __name__ == '__main__':
    unittest.main()