import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.response import Response
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestCSRFView(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.scheme = "http"
        self.request.session = {'csrf_token': 'valid_token'}

    def test_csrf_view_fails_on_missing_csrf_token(self):
        self.request.method = 'PUT'
        self.request.headers = {}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_csrf_view_fails_on_invalid_csrf_token(self):
        self.request.method = 'PUT'
        self.request.headers = {'X-CSRF-Token': 'invalid_token'}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_csrf_view_succeeds_on_valid_csrf_token(self):
        self.request.method = 'PUT'
        self.request.headers = {'X-CSRF-Token': 'valid_token'}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        response = view(None, self.request)
        self.assertIsInstance(response, Response)

    def test_csrf_view_fails_on_non_put_method(self):
        self.request.method = 'GET'
        self.request.headers = {'X-CSRF-Token': 'valid_token'}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        response = view(None, self.request)
        self.assertIsInstance(response, Response)  # Assuming GET does not require CSRF

    def test_csrf_view_fails_on_empty_csrf_token(self):
        self.request.method = 'PUT'
        self.request.headers = {'X-CSRF-Token': ''}
        view = self.config._derive_view(lambda req: Response(), require_csrf=True)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)