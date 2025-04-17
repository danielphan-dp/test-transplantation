import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_no_authorization_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_auth_scheme(self):
        self.request.headers['Authorization'] = 'Bearer %s' % base64.b64encode(
            bytes_('chrisr:password')
        ).decode('ascii')
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_malformed_authorization_header(self):
        self.request.headers['Authorization'] = 'Basic'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic InvalidBase64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_valid_basic_auth(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes_('chrisr:password')
        ).decode('ascii')
        fn = extract_http_basic_credentials
        credentials = fn(self.request)
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials.username, 'chrisr')
        self.assertEqual(credentials.password, 'password')

    def test_invalid_utf8_decoding(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes_('chrisr:\x80\x81password')
        ).decode('ascii')
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

if __name__ == '__main__':
    unittest.main()