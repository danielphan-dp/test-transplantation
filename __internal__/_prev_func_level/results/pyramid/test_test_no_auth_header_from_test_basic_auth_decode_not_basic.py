import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_no_auth_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_not_basic(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_missing_credentials(self):
        self.request.headers['Authorization'] = 'Basic '
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_invalid_format(self):
        self.request.headers['Authorization'] = 'Basic invalid_format'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_valid_credentials(self):
        import base64
        credentials = base64.b64encode(b'username:password').decode('utf-8')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        fn = extract_http_basic_credentials
        result = fn(self.request)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'username')
        self.assertEqual(result.password, 'password')

    def test_auth_header_invalid_base64(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))