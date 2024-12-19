import unittest
from pyramid.exceptions import BadCSRFOrigin
from pyramid.response import Response
from pyramid.request import Request

class TestView(unittest.TestCase):

    def _makeRequest(self):
        request = Request.blank('/')
        return request

    def test_csrf_view_passes_on_good_referrer(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest()
        request.method = "POST"
        request.scheme = "https"
        request.host_port = "443"
        request.domain = "example.com"
        request.referrer = "https://example.com/"
        view = self.config._derive_view(inner_view, require_csrf=True)
        response = view(None, request)
        self.assertEqual(response.text, "Success")

    def test_csrf_view_fails_on_missing_referrer(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest()
        request.method = "POST"
        request.scheme = "https"
        request.host_port = "443"
        request.domain = "example.com"
        request.referrer = None
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFOrigin, lambda: view(None, request))

    def test_csrf_view_fails_on_empty_referrer(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest()
        request.method = "POST"
        request.scheme = "https"
        request.host_port = "443"
        request.domain = "example.com"
        request.referrer = ""
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFOrigin, lambda: view(None, request))

    def test_csrf_view_fails_on_non_https(self):
        def inner_view(request):  # pragma: no cover
            return Response("Success")

        request = self._makeRequest()
        request.method = "POST"
        request.scheme = "http"
        request.host_port = "80"
        request.domain = "example.com"
        request.referrer = "https://example.com/"
        view = self.config._derive_view(inner_view, require_csrf=True)
        self.assertRaises(BadCSRFOrigin, lambda: view(None, request))