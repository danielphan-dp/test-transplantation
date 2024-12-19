import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest

class TestView(unittest.TestCase):

    def test_csrf_view_allows_POST_with_valid_token(self):
        response = Response()
        
        def inner_view(request):
            return response

        request = DummyRequest()
        request.method = 'POST'
        request.headers['X-CSRF-Token'] = 'valid_token'
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is response)

    def test_csrf_view_rejects_POST_with_invalid_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.headers['X-CSRF-Token'] = 'invalid_token'
        
        def inner_view(request):
            raise BadCSRFToken("Invalid CSRF token")

        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_rejects_POST_without_token(self):
        request = DummyRequest()
        request.method = 'POST'
        
        def inner_view(request):
            raise BadCSRFToken("Missing CSRF token")

        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_allows_OPTIONS_method(self):
        response = Response()
        
        def inner_view(request):
            return response

        request = DummyRequest()
        request.method = 'OPTIONS'
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is response)