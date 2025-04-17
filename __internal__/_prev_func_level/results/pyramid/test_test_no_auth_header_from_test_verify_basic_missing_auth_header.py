import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_no_auth_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'InvalidFormat'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_without_basic(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_empty_credentials(self):
        self.request.headers['Authorization'] = 'Basic '
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_invalid_base64(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_valid_credentials(self):
        import base64
        credentials = base64.b64encode(b'username:password').decode('utf-8')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        fn = extract_http_basic_credentials
        result = fn(self.request)
        self.assertEqual(result.username, 'username')
        self.assertEqual(result.password, 'password')

if __name__ == '__main__':
    unittest.main()