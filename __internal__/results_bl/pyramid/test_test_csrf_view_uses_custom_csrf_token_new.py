import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.config import Configurator

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.response = DummyResponse()

    def test_view_with_valid_csrf_token(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'valid_token'}
        request.POST = {'DUMMY': 'valid_token'}
        self.config.set_default_csrf_options(require_csrf=True, token='DUMMY')
        view = self.config._derive_view(inner_view)
        result = view(None, request)
        self.assertIs(result, self.response)

    def test_view_with_invalid_csrf_token(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'valid_token'}
        request.POST = {'DUMMY': 'invalid_token'}
        self.config.set_default_csrf_options(require_csrf=True, token='DUMMY')
        view = self.config._derive_view(inner_view)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_view_with_missing_csrf_token(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {}
        request.POST = {}
        self.config.set_default_csrf_options(require_csrf=True, token='DUMMY')
        view = self.config._derive_view(inner_view)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_view_with_get_request(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'GET'
        request.session = {'csrf_token': 'valid_token'}
        request.POST = {}
        self.config.set_default_csrf_options(require_csrf=True, token='DUMMY')
        view = self.config._derive_view(inner_view)
        result = view(None, request)
        self.assertIs(result, self.response)

    def test_view_with_no_csrf_required(self):
        def inner_view(request):
            return self.response

        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'valid_token'}
        request.POST = {'DUMMY': 'valid_token'}
        self.config.set_default_csrf_options(require_csrf=False)
        view = self.config._derive_view(inner_view)
        result = view(None, request)
        self.assertIs(result, self.response)