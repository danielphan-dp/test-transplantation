import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_basic_auth(self):
        inputs = b'user:password'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (b'user'.decode('utf-8'), b'password'.decode('utf-8')),
        )

    def test_missing_authorization_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_utf8_username_password(self):
        inputs = (b'm\xc3\xb6rk\xc3\xb6:' b'm\xc3\xb6rk\xc3\xb6password')
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (b'm\xc3\xb6rk\xc3\xb6'.decode('utf-8'), b'm\xc3\xb6rk\xc3\xb6password'.decode('utf-8')),
        )

    def test_partial_credentials(self):
        inputs = b'user:'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (b'user'.decode('utf-8'), b''.decode('utf-8')),
        )

    def test_no_colon_in_credentials(self):
        inputs = b'userpassword'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

if __name__ == '__main__':
    unittest.main()