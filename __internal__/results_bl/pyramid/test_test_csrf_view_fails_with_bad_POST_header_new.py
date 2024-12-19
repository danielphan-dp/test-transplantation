import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.response import Response
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestView(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.scheme = "http"
        self.request.method = 'POST'
        self.request.session = {'csrf_token': 'valid_token'}

    def test_csrf_view_fails_with_missing_POST_header(self):
        from pyramid.view import view_config

        @view_config(require_csrf=True)
        def inner_view(request):
            return Response("Success")

        view = self.config._derive_view(inner_view, require_csrf=True)
        self.request.headers = {}
        self.assertRaises(BadCSRFToken, lambda: view(None, self.request))

    def test_csrf_view_fails_with_invalid_token(self):
        from pyramid.view import view_config

        @view_config(require_csrf=True)
        def inner_view(request):
            return Response("Success")

        view = self.config._derive_view(inner_view, require_csrf=True)
        self.request.headers = {'X-CSRF-Token': 'invalid_token'}
        self.assertRaises(BadCSRFToken, lambda: view(None, self.request))

    def test_csrf_view_succeeds_with_valid_token(self):
        from pyramid.view import view_config

        @view_config(require_csrf=True)
        def inner_view(request):
            return Response("Success")

        view = self.config._derive_view(inner_view, require_csrf=True)
        self.request.headers = {'X-CSRF-Token': 'valid_token'}
        response = view(None, self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Success")