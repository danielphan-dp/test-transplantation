import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def _get_func(self):
        return extract_http_basic_credentials

    def test_not_a_basic_auth_scheme(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'OtherScheme %s' % base64.b64encode(
            bytes_('chrisr:password')
        ).decode('ascii')
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_empty_authorization_header(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = ''
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_missing_authorization_header(self):
        request = testing.DummyRequest()
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_invalid_base64_encoding(self):
        request = testing.DummyRequest()
        request.headers['Authorization'] = 'Basic invalid_base64'
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_valid_basic_auth(self):
        request = testing.DummyRequest()
        credentials = base64.b64encode(b'chrisr:password').decode('ascii')
        request.headers['Authorization'] = 'Basic %s' % credentials
        fn = self._get_func()
        self.assertEqual(fn(request), ('chrisr', 'password'))

    def test_partial_basic_auth(self):
        request = testing.DummyRequest()
        credentials = base64.b64encode(b'chrisr:').decode('ascii')
        request.headers['Authorization'] = 'Basic %s' % credentials
        fn = self._get_func()
        self.assertEqual(fn(request), ('chrisr', ''))

    def test_auth_with_special_characters(self):
        request = testing.DummyRequest()
        credentials = base64.b64encode(b'chr!s:r@password').decode('ascii')
        request.headers['Authorization'] = 'Basic %s' % credentials
        fn = self._get_func()
        self.assertEqual(fn(request), ('chr!s', 'r@password'))