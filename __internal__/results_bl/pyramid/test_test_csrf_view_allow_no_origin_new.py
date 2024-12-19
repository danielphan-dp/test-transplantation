import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.view import view_config

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = DummyConfig()
        self.response = DummyResponse()

    def test_csrf_view_invalid_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True)
        request = DummyRequest()
        request.method = 'POST'
        request.session = DummySession({'csrf_token': 'invalid'})
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(inner_view, require_csrf=True)

        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_missing_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True)
        request = DummyRequest()
        request.method = 'POST'
        request.session = DummySession({})
        request.POST = {}
        view = self.config._derive_view(inner_view, require_csrf=True)

        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_allow_origin(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, allow_no_origin=False)
        request = DummyRequest()
        request.method = 'POST'
        request.session = DummySession({'csrf_token': 'foo'})
        request.POST = {'csrf_token': 'foo'}
        request.origin = 'http://example.com'
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is self.response)

    def test_csrf_view_no_origin_with_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, allow_no_origin=False)
        request = DummyRequest()
        request.method = 'POST'
        request.session = DummySession({'csrf_token': 'foo'})
        request.POST = {'csrf_token': 'foo'}
        request.origin = None
        view = self.config._derive_view(inner_view, require_csrf=True)

        with self.assertRaises(BadCSRFOrigin):
            view(None, request)

class DummyConfig:
    def set_default_csrf_options(self, require_csrf, allow_no_origin):
        self.require_csrf = require_csrf
        self.allow_no_origin = allow_no_origin

    def _derive_view(self, view, require_csrf):
        def wrapped_view(context, request):
            if require_csrf and request.method == 'POST':
                token = request.POST.get('csrf_token')
                if token != request.session.get('csrf_token'):
                    raise BadCSRFToken()
                if not self.allow_no_origin and request.origin is None:
                    raise BadCSRFOrigin()
            return view(request)
        return wrapped_view

class DummySession:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.data.get(key)