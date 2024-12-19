import unittest
from pyramid.exceptions import BadCSRFOrigin, BadCSRFToken
from pyramid.response import Response
from pyramid.request import Request

class TestView(unittest.TestCase):

    def _makeRequest(self, method='GET', origin='https://example.com'):
        request = Request.blank('/')
        request.method = method
        request.headers = {'Origin': origin}
        return request

    def test_csrf_view_fails_on_invalid_token(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest(method='POST', origin='https://example.com')
        request.registry.settings = {'csrf_token': 'invalid_token'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFToken, lambda: view(None, request))

    def test_csrf_view_passes_on_valid_token(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest(method='POST', origin='https://example.com')
        request.registry.settings = {'csrf_token': 'valid_token'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        response = view(None, request)
        self.assertEqual(response.status_code, 200)

    def test_csrf_view_fails_on_missing_origin(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest(method='POST', origin=None)
        request.registry.settings = {}
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFOrigin, lambda: view(None, request))

    def test_csrf_view_fails_on_empty_origin(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest(method='POST', origin='')
        request.registry.settings = {}
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFOrigin, lambda: view(None, request))