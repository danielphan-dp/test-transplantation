import unittest
from pyramid.authentication import extract_http_basic_credentials
from pyramid.testing import DummyRequest

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.fn = extract_http_basic_credentials

    def test_no_auth_header(self):
        self.assertIsNone(self.fn(self.request))

    def test_empty_auth_header(self):
        self.request.headers['Authorization'] = ''
        self.assertIsNone(self.fn(self.request))

    def test_invalid_auth_header_format(self):
        self.request.headers['Authorization'] = 'InvalidFormat'
        self.assertIsNone(self.fn(self.request))

    def test_missing_credentials(self):
        self.request.headers['Authorization'] = 'Basic ' + base64.b64encode(b':').decode('utf-8')
        self.assertIsNone(self.fn(self.request))

    def test_valid_credentials(self):
        self.request.headers['Authorization'] = 'Basic ' + base64.b64encode(b'username:password').decode('utf-8')
        self.assertEqual(self.fn(self.request), ('username', 'password'))

    def test_auth_header_with_extra_spaces(self):
        self.request.headers['Authorization'] = '  Basic  ' + base64.b64encode(b'username:password').decode('utf-8') + '  '
        self.assertEqual(self.fn(self.request), ('username', 'password'))