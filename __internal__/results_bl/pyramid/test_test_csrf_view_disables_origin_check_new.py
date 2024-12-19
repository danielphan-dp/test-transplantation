import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken, BadCSRFOrigin

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = pyramid.testing.setUp()
        self.response = Response()

    def tearDown(self):
        pyramid.testing.tearDown()

    def test_csrf_view_with_valid_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, check_origin=True)
        request = self._makeRequest()
        request.method = 'POST'
        request.session = DummySession({'csrf_token': 'valid_token'})
        request.POST = {'csrf_token': 'valid_token'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is self.response)

    def test_csrf_view_with_invalid_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, check_origin=True)
        request = self._makeRequest()
        request.method = 'POST'
        request.session = DummySession({'csrf_token': 'valid_token'})
        request.POST = {'csrf_token': 'invalid_token'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_with_no_token(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, check_origin=True)
        request = self._makeRequest()
        request.method = 'POST'
        request.session = DummySession({})
        request.POST = {}
        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_csrf_view_with_invalid_origin(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, check_origin=True)
        request = self._makeRequest()
        request.method = 'POST'
        request.headers = {"Origin": "https://evil-example.com"}
        request.session = DummySession({'csrf_token': 'foo'})
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        with self.assertRaises(BadCSRFOrigin):
            view(None, request)

    def test_csrf_view_with_valid_origin(self):
        def inner_view(request):
            return self.response

        self.config.set_default_csrf_options(require_csrf=True, check_origin=True)
        request = self._makeRequest()
        request.method = 'POST'
        request.headers = {"Origin": "https://example.com"}
        request.session = DummySession({'csrf_token': 'foo'})
        request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(inner_view, require_csrf=True)
        result = view(None, request)
        self.assertTrue(result is self.response)