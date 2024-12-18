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
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_missing_username_password(self):
        self.request.headers['Authorization'] = 'Basic ' + b64encode(b':').decode('utf-8')
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_valid_credentials(self):
        self.request.headers['Authorization'] = 'Basic ' + b64encode(b'username:password').decode('utf-8')
        fn = extract_http_basic_credentials
        credentials = fn(self.request)
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials.username, 'username')
        self.assertEqual(credentials.password, 'password')

if __name__ == '__main__':
    unittest.main()