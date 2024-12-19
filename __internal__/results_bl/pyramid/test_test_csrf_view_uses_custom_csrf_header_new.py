import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse

class TestView(unittest.TestCase):

    def setUp(self):
        self.response = DummyResponse()
        self.request = DummyRequest()
        self.request.method = 'POST'
        self.request.session = {'csrf_token': 'valid_token'}
        self.request.headers = {'DUMMY': 'valid_token'}

    def test_view_with_valid_csrf_token(self):
        self.config.set_default_csrf_options(require_csrf=True, header='DUMMY')
        view = self.config._derive_view(lambda request: self.response)
        result = view(None, self.request)
        self.assertIs(result, self.response)

    def test_view_with_invalid_csrf_token(self):
        self.request.headers['DUMMY'] = 'invalid_token'
        self.config.set_default_csrf_options(require_csrf=True, header='DUMMY')
        view = self.config._derive_view(lambda request: self.response)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_view_with_missing_csrf_token(self):
        del self.request.headers['DUMMY']
        self.config.set_default_csrf_options(require_csrf=True, header='DUMMY')
        view = self.config._derive_view(lambda request: self.response)
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_view_with_get_request(self):
        self.request.method = 'GET'
        self.config.set_default_csrf_options(require_csrf=True, header='DUMMY')
        view = self.config._derive_view(lambda request: self.response)
        result = view(None, self.request)
        self.assertIs(result, self.response)

    def test_view_without_csrf_required(self):
        self.config.set_default_csrf_options(require_csrf=False)
        view = self.config._derive_view(lambda request: self.response)
        result = view(None, self.request)
        self.assertIs(result, self.response)