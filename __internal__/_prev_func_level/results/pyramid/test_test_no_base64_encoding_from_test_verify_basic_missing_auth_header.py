import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_missing_auth_header(self):
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'InvalidFormat'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_auth_header_without_basic(self):
        self.request.headers['Authorization'] = 'Bearer token'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_auth_header_with_empty_credentials(self):
        self.request.headers['Authorization'] = 'Basic ' + base64.b64encode(b':').decode('utf-8')
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_auth_header_with_invalid_base64(self):
        self.request.headers['Authorization'] = 'Basic ' + 'invalid_base64'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_auth_header_with_valid_credentials(self):
        username = 'user'
        password = 'pass'
        self.request.headers['Authorization'] = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
        credentials = extract_http_basic_credentials(self.request)
        self.assertEqual(credentials.username, username)
        self.assertEqual(credentials.password, password)

if __name__ == '__main__':
    unittest.main()