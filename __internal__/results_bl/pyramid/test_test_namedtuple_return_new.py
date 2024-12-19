import base64
import unittest
from pyramid.authentication import extract_http_basic_credentials
from pyramid.testing import DummyRequest

class TestAuthentication(unittest.TestCase):

    def test_empty_authorization_header(self):
        request = DummyRequest()
        request.headers['Authorization'] = ''
        fn = extract_http_basic_credentials
        result = fn(request)
        self.assertIsNone(result)

    def test_invalid_authorization_header_format(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Bearer token'
        fn = extract_http_basic_credentials
        result = fn(request)
        self.assertIsNone(result)

    def test_malformed_base64_credentials(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic malformed_base64'
        fn = extract_http_basic_credentials
        result = fn(request)
        self.assertIsNone(result)

    def test_valid_authorization_header_with_special_characters(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('user:pa$$word')
        ).decode('ascii')
        fn = extract_http_basic_credentials
        result = fn(request)
        self.assertEqual(result.username, 'user')
        self.assertEqual(result.password, 'pa$$word')

    def test_authorization_header_with_non_ascii_characters(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic %s' % base64.b64encode(
            bytes('用户:密码')
        ).decode('ascii')
        fn = extract_http_basic_credentials
        result = fn(request)
        self.assertEqual(result.username, '用户')
        self.assertEqual(result.password, '密码')