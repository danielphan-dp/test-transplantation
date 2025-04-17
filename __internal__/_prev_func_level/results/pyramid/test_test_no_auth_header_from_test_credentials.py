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
        self.request.headers['Authorization'] = 'InvalidHeaderFormat'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_without_basic(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_empty_basic(self):
        self.request.headers['Authorization'] = 'Basic '
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_non_base64(self):
        self.request.headers['Authorization'] = 'Basic non_base64_string'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_auth_header_with_valid_basic_credentials(self):
        import base64
        username = 'user'
        password = 'pass'
        credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('ascii')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        fn = extract_http_basic_credentials
        result = fn(self.request)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, username)
        self.assertEqual(result.password, password)

    def test_auth_header_with_invalid_utf8(self):
        self.request.headers['Authorization'] = 'Basic ' + base64.b64encode(b'\x80\x81').decode('ascii')
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

if __name__ == '__main__':
    unittest.main()