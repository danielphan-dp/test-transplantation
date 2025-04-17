import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_credentials_utf8(self):
        inputs = 'username:password'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            ('username', 'password'),
        )

    def test_valid_credentials_latin1(self):
        inputs = b'm\xc3\xb6rk\xc3\xb6:password'.decode('utf-8')
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('latin-1')).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (b'm\xc3\xb6rk\xc3\xb6'.decode('utf-8'), 'password'),
        )

    def test_missing_authorization_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_no_colon_in_credentials(self):
        inputs = 'usernamepassword'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_empty_credentials(self):
        inputs = ':'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(fn(self.request), ('', ''))

if __name__ == '__main__':
    unittest.main()