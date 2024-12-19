import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_empty_authorization_header(self):
        self.request.headers['Authorization'] = ''
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = extract_http_basic_credentials
        self.assertIsNone(fn(self.request))

    def test_missing_password(self):
        inputs = b'm\xc3\xb6rk\xc3\xb6:'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(fn(self.request), (b'm\xc3\xb6rk\xc3\xb6'.decode('utf-8'), None))

    def test_missing_username(self):
        inputs = b':m\xc3\xb6rk\xc3\xb6password'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(fn(self.request), (None, b'm\xc3\xb6rk\xc3\xb6password'.decode('utf-8')))

    def test_special_characters_in_credentials(self):
        inputs = b'username!@#$%^&*()_+:' b'password!@#$%^&*()_+'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        fn = extract_http_basic_credentials
        self.assertEqual(
            fn(self.request),
            (
                b'username!@#$%^&*()_+'.decode('utf-8'),
                b'password!@#$%^&*()_+'.decode('utf-8'),
            ),
        )