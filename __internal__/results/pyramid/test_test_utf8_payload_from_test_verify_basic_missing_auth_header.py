import base64
import unittest
from pyramid import testing
from pyramid.authentication import extract_http_basic_credentials

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()

    def test_valid_basic_auth(self):
        inputs = b'user:password'
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result, (b'user'.decode('utf-8'), b'password'.decode('utf-8')))

    def test_missing_auth_header(self):
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'Bearer token'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_invalid_base64_encoding(self):
        self.request.headers['Authorization'] = 'Basic invalid_base64'
        result = extract_http_basic_credentials(self.request)
        self.assertIsNone(result)

    def test_utf8_username_password(self):
        inputs = (b'm\xc3\xb6rk\xc3\xb6:' b'm\xc3\xb6rk\xc3\xb6password')
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result, (b'm\xc3\xb6rk\xc3\xb6'.decode('utf-8'), b'm\xc3\xb6rk\xc3\xb6password'.decode('utf-8')))

    def test_latin1_username_password(self):
        inputs = (b'm\xf6rk\xf6:' b'm\xf6rk\xf6password')
        self.request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs).decode('latin-1')
        )
        result = extract_http_basic_credentials(self.request)
        self.assertEqual(result, (b'm\xf6rk\xf6'.decode('latin-1'), b'm\xf6rk\xf6password'.decode('latin-1')))

if __name__ == '__main__':
    unittest.main()