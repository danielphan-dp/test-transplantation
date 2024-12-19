import unittest
from pyramid.authentication import extract_http_basic_credentials
from pyramid.testing import DummyRequest

class TestExtractHttpBasicCredentials(unittest.TestCase):

    def setUp(self):
        self.fn = extract_http_basic_credentials

    def test_valid_credentials(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='  # base64 for 'username:password'
        credentials = self.fn(request)
        self.assertEqual(credentials, ('username', 'password'))

    def test_empty_authorization_header(self):
        request = DummyRequest()
        request.headers['Authorization'] = ''
        self.assertIsNone(self.fn(request))

    def test_missing_authorization_header(self):
        request = DummyRequest()
        self.assertIsNone(self.fn(request))

    def test_invalid_base64_encoding(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic invalid_base64'
        self.assertIsNone(self.fn(request))

    def test_non_basic_auth_scheme(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Bearer token'
        self.assertIsNone(self.fn(request))

    def test_partial_base64_credentials(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic dXNlcm5hbWU6'  # base64 for 'username:'
        credentials = self.fn(request)
        self.assertEqual(credentials, ('username', None))

    def test_base64_with_special_characters(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic ' + base64.b64encode(b'user:pass@123').decode('utf-8')
        credentials = self.fn(request)
        self.assertEqual(credentials, ('user', 'pass@123'))