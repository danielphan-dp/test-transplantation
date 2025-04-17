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

    def test_invalid_authorization_format(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_missing_credentials(self):
        self.request.headers['Authorization'] = 'Basic '
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_valid_credentials(self):
        credentials = base64.b64encode(b'username:password').decode('ascii')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        fn = extract_http_basic_credentials
        result = fn(self.request)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'username')
        self.assertEqual(result.password, 'password')

    def test_invalid_utf8_decoding(self):
        invalid_utf8 = base64.b64encode(b'username:\xff').decode('ascii')
        self.request.headers['Authorization'] = f'Basic {invalid_utf8}'
        fn = extract_http_basic_credentials
        result = fn(self.request)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'username')
        self.assertEqual(result.password, '\xff')

    def test_no_colon_in_credentials(self):
        credentials = base64.b64encode(b'usernamepassword').decode('ascii')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))