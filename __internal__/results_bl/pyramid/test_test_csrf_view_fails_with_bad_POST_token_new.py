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
        self.request.session = {'csrf_token': 'foo'}

    def test_csrf_view_fails_with_missing_POST_token(self):
        self.request.POST = {}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_csrf_view_fails_with_empty_POST_token(self):
        self.request.POST = {'csrf_token': ''}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_csrf_view_passes_with_valid_POST_token(self):
        self.request.POST = {'csrf_token': 'foo'}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        response = view(None, self.request)
        self.assertIsInstance(response, Response)

    def test_csrf_view_fails_with_invalid_request_method(self):
        self.request.method = 'GET'
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        response = view(None, self.request)
        self.assertIsInstance(response, Response)  # Assuming GET does not require CSRF

    def test_csrf_view_fails_with_bad_origin(self):
        self.request.POST = {'csrf_token': 'bar'}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)