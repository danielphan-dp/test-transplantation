import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.response import Response
from pyramid.request import Request
from pyramid.testing import DummySession

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = self._makeConfig()
        self.request = self._makeRequest()
        self.request.scheme = "http"
        self.request.method = 'POST'
        self.request.session = DummySession({'csrf_token': 'foo'})
        self.config.set_default_csrf_options(require_csrf=True)

    def _makeConfig(self):
        # Mock configuration setup
        pass

    def _makeRequest(self):
        # Mock request setup
        return Request()

    def test_csrf_view_enabled_by_default(self):
        def inner_view(request):  # pragma: no cover
            return Response("Inner View")

        view = self.config._derive_view(inner_view)
        self.assertRaises(BadCSRFToken, lambda: view(None, self.request))

    def test_csrf_view_with_invalid_token(self):
        self.request.session = DummySession({'csrf_token': 'invalid'})
        def inner_view(request):  # pragma: no cover
            return Response("Inner View")

        view = self.config._derive_view(inner_view)
        self.assertRaises(BadCSRFToken, lambda: view(None, self.request))

    def test_csrf_view_with_no_token(self):
        self.request.session = DummySession({})
        def inner_view(request):  # pragma: no cover
            return Response("Inner View")

        view = self.config._derive_view(inner_view)
        self.assertRaises(BadCSRFToken, lambda: view(None, self.request))

    def test_csrf_view_with_get_method(self):
        self.request.method = 'GET'
        def inner_view(request):  # pragma: no cover
            return Response("Inner View")

        view = self.config._derive_view(inner_view)
        response = view(None, self.request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.text, "Inner View")