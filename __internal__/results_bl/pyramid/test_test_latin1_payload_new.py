import base64
import unittest
from pyramid.testing import DummyRequest
from pyramid.authentication import extract_http_basic_credentials

class TestAuthentication(unittest.TestCase):

    def _get_func(self):
        return extract_http_basic_credentials

    def test_empty_authorization_header(self):
        request = DummyRequest()
        request.headers['Authorization'] = ''
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_invalid_base64_encoding(self):
        request = DummyRequest()
        request.headers['Authorization'] = 'Basic invalid_base64'
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_no_colon_in_credentials(self):
        request = DummyRequest()
        inputs = 'usernamewithoutcolon'
        request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = self._get_func()
        self.assertIsNone(fn(request))

    def test_special_characters_in_credentials(self):
        request = DummyRequest()
        inputs = 'user@name:pass#word'
        request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = self._get_func()
        self.assertEqual(
            fn(request),
            ('user@name', 'pass#word')
        )

    def test_unicode_credentials(self):
        request = DummyRequest()
        inputs = 'mörkör:mörkörpassword'
        request.headers['Authorization'] = 'Basic %s' % (
            base64.b64encode(inputs.encode('utf-8')).decode('utf-8')
        )
        fn = self._get_func()
        self.assertEqual(
            fn(request),
            ('mörkör', 'mörkörpassword')
        )