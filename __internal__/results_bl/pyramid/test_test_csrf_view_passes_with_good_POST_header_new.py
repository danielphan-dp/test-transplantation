import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.view import view_config

class TestCSRFView(unittest.TestCase):

    def _makeRequest(self, method='POST', csrf_token='foo'):
        request = DummyRequest()
        request.method = method
        request.session = DummySession({'csrf_token': csrf_token})
        request.headers = {'X-CSRF-Token': csrf_token}
        return request

    def test_csrf_view_fails_with_bad_POST_header(self):
        response = DummyResponse()

        def inner_view(request):
            return response

        request = self._makeRequest(csrf_token='wrong_token')
        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_fails_with_missing_POST_header(self):
        response = DummyResponse()

        def inner_view(request):
            return response

        request = self._makeRequest()
        del request.headers['X-CSRF-Token']
        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_passes_with_good_POST_header(self):
        response = DummyResponse()

        def inner_view(request):
            return response

        request = self._makeRequest()
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is response)

    def test_csrf_view_passes_with_different_csrf_token(self):
        response = DummyResponse()

        def inner_view(request):
            return response

        request = self._makeRequest(csrf_token='bar')
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is response)