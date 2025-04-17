import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_missing_auth_header(self):
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Bearer some_token'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_no_colon_in_credentials(self):
        inputs = b'myusername' + b'myusernamepassword'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_valid_credentials(self):
        inputs = b'myusername:myusernamepassword'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (b'myusername'.decode('utf-8'), b'myusernamepassword'.decode('utf-8'))
        )

    def test_utf8_credentials(self):
        inputs = (b'm\xc3\xb6rk\xc3\xb6:' b'm\xc3\xb6rk\xc3\xb6password').decode('utf-8')
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (
                b'm\xc3\xb6rk\xc3\xb6'.decode('utf-8'),
                b'm\xc3\xb6rk\xc3\xb6password'.decode('utf-8'),
            ),
        )