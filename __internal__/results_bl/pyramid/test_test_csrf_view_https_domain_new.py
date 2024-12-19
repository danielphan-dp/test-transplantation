import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.view import view_config

class TestCSRFView(unittest.TestCase):

    def setUp(self):
        self.response = DummyResponse()

    def inner_view(self, request):
        return self.response

    def test_csrf_view_invalid_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'invalid_token'}
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(self.inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_missing_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'foo'}
        request.POST = {}
        view = self.config._derive_view(self.inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_http_domain(self):
        request = DummyRequest()
        request.scheme = "http"
        request.domain = "example.com"
        request.host_port = "80"
        request.referrer = "http://example.com/login/"
        request.method = 'POST'
        request.session = {'csrf_token': 'foo'}
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(self.inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is self.response)

    def test_csrf_view_https_no_referrer(self):
        request = DummyRequest()
        request.scheme = "https"
        request.domain = "example.com"
        request.host_port = "443"
        request.method = 'POST'
        request.session = {'csrf_token': 'foo'}
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(self.inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is self.response)