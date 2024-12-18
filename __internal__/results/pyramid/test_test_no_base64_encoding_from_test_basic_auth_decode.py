import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_no_authorization_header(self):
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_missing_credentials(self):
        self.request.headers['Authorization'] = 'Basic '
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_valid_credentials(self):
        import base64
        credentials = base64.b64encode(b'nkim:pwd').decode('utf-8')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'nkim')
        self.assertEqual(result.password, 'pwd')

    def test_credentials_with_extra_colon(self):
        import base64
        credentials = base64.b64encode(b'nkim:pwd:extra').decode('utf-8')
        self.request.headers['Authorization'] = f'Basic {credentials}'
        self.assertIsNone(extract_http_basic_credentials(self.request))

if __name__ == '__main__':
    unittest.main()