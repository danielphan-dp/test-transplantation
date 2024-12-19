import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.config import Configurator

class TestCSRFView(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.response = DummyResponse()

    def test_csrf_view_with_invalid_token(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'invalid_token'}
        self.config.set_default_csrf_options(require_csrf=True, safe_methods=['PUT'])
        view = self.config._derive_view(inner_view)

        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_with_missing_token(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {}
        self.config.set_default_csrf_options(require_csrf=True, safe_methods=['PUT'])
        view = self.config._derive_view(inner_view)

        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_with_safe_method(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'PUT'
        request.session = {'csrf_token': 'foo'}
        self.config.set_default_csrf_options(require_csrf=True, safe_methods=['PUT'])
        view = self.config._derive_view(inner_view)
        result = view(None, request)
        self.assertTrue(result is self.response)

    def test_csrf_view_with_unsafe_method(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'DELETE'
        request.session = {'csrf_token': 'foo'}
        self.config.set_default_csrf_options(require_csrf=True, safe_methods=['PUT'])
        view = self.config._derive_view(inner_view)

        with self.assertRaises(BadCSRFToken):
            view(None, request)