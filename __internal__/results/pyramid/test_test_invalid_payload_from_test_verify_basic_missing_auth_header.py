import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b'username:password').decode('ascii')
        username, password = extract_http_basic_credentials(self.request)
        self.assertEqual(username, 'username')
        self.assertEqual(password, 'password')

    def test_missing_auth_header(self):
        self.request.headers.pop('Authorization', None)
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Bearer some_token'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_no_colon_in_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b'usernamewithoutcolon').decode('ascii')
        self.assertIsNone(extract_http_basic_credentials(self.request))

    def test_empty_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(b':').decode('ascii')
        username, password = extract_http_basic_credentials(self.request)
        self.assertEqual(username, '')
        self.assertEqual(password, '')

if __name__ == '__main__':
    unittest.main()