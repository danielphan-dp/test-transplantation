import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_missing_authorization_header(self):
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'InvalidHeaderFormat'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_non_basic_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_base64_decoding_failure(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_valid_credentials(self):
        import base64
        valid_credentials = base64.b64encode(b'username:password').decode('utf-8')
        self.request.headers['Authorization'] = f'Basic {valid_credentials}'
        credentials = extract_http_basic_credentials(self.request)
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials.username, 'username')
        self.assertEqual(credentials.password, 'password')

if __name__ == '__main__':
    unittest.main()