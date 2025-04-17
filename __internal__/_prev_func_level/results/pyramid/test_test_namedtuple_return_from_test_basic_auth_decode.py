import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_basic_auth(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr:pass', 'utf-8')
        ).decode('ascii')
        fn = self._get_func()
        result = fn(self.request)

        self.assertEqual(result.username, 'chrisr')
        self.assertEqual(result.password, 'pass')

    def test_missing_authorization_header(self):
        fn = self._get_func()
        result = fn(self.request)

        self.assertIsNone(result)

    def test_invalid_auth_method(self):
        self.request.headers['Authorization'] = 'Bearer token'
        fn = self._get_func()
        result = fn(self.request)

        self.assertIsNone(result)

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        fn = self._get_func()
        result = fn(self.request)

        self.assertIsNone(result)

    def test_no_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes(':', 'utf-8')
        ).decode('ascii')
        fn = self._get_func()
        result = fn(self.request)

        self.assertIsNone(result)

    def test_partial_credentials(self):
        self.request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('chrisr', 'utf-8')
        ).decode('ascii')
        fn = self._get_func()
        result = fn(self.request)

        self.assertIsNone(result)

    def _get_func(self):
        from pyramid.authentication import extract_http_basic_credentials
        return extract_http_basic_credentials

if __name__ == '__main__':
    unittest.main()