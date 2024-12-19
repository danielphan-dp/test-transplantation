import unittest
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.config import Configurator

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.response = DummyResponse()

    def test_view_with_valid_request(self):
        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'valid_token'}
        self.config.set_default_csrf_options(require_csrf=True)
        view = self.config._derive_view(lambda req: self.response)
        result = view(None, request)
        self.assertIs(result, self.response)

    def test_view_with_invalid_csrf_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'invalid_token'}
        self.config.set_default_csrf_options(require_csrf=True)
        view = self.config._derive_view(lambda req: self.response)
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_view_with_get_request(self):
        request = DummyRequest()
        request.method = 'GET'
        self.config.set_default_csrf_options(require_csrf=True)
        view = self.config._derive_view(lambda req: self.response)
        result = view(None, request)
        self.assertIs(result, self.response)

    def test_view_with_no_csrf_required(self):
        request = DummyRequest()
        request.method = 'POST'
        self.config.set_default_csrf_options(require_csrf=False)
        view = self.config._derive_view(lambda req: self.response)
        result = view(None, request)
        self.assertIs(result, self.response)

    def test_view_with_callback_returning_false(self):
        def callback(request):
            return False

        self.config.set_default_csrf_options(require_csrf=True, callback=callback)
        request = DummyRequest()
        request.method = 'POST'
        request.session = {'csrf_token': 'foo'}
        view = self.config._derive_view(lambda req: self.response)
        result = view(None, request)
        self.assertIs(result, self.response)