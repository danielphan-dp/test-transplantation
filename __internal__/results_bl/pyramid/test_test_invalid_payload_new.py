import base64
import unittest
from pyramid import testing

class TestAuthentication(unittest.TestCase):

    def _get_func(self):
        from pyramid.authentication import extract_http_basic_credentials
        return extract_http_basic_credentials

    def test_valid_credentials(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b'username:password'
        ).decode('ascii')
        fn = self._get_func()
        credentials = fn(request)
        self.assertEqual(credentials, ('username', 'password'))

    def test_missing_authorization_header(self):
        request = testing.DummyRequest()
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_invalid_base64_encoding(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic invalid_base64'
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_empty_credentials(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b':'
        ).decode('ascii')
        fn = self._get_func()
        credentials = fn(request)
        self.assertEqual(credentials, ('', ''))

    def test_only_username(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b'username:'
        ).decode('ascii')
        fn = self._get_func()
        credentials = fn(request)
        self.assertEqual(credentials, ('username', ''))

    def test_only_password(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            b':password'
        ).decode('ascii')
        fn = self._get_func()
        credentials = fn(request)
        self.assertEqual(credentials, ('', 'password'))