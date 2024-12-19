import os
import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.renderers import null_renderer
from pyramid.response import Response
from pyramid.testing import DummyRequest

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)
        self.view = self._getViewCallable(self.config)

    def _makeOne(self, **kwargs):
        from pyramid.config import Configurator
        return Configurator(**kwargs)

    def _getViewCallable(self, config):
        return config.make_wsgi_app()

    def _makeRequest(self, config):
        return DummyRequest()

    def test_view_with_valid_csrf_token(self):
        request = self._makeRequest(self.config)
        request.method = 'POST'
        request.headers = {'X-CSRF-Token': 'foo'}
        request.session = DummySession({'csrf_token': 'foo'})
        response = self.view(None, request)
        self.assertIsInstance(response, Response)

    def test_view_with_invalid_csrf_token(self):
        request = self._makeRequest(self.config)
        request.method = 'POST'
        request.headers = {'X-CSRF-Token': 'bar'}
        request.session = DummySession({'csrf_token': 'foo'})
        with self.assertRaises(BadCSRFToken):
            self.view(None, request)

    def test_view_with_missing_csrf_token_header(self):
        request = self._makeRequest(self.config)
        request.method = 'POST'
        request.headers = {}
        request.session = DummySession({'csrf_token': 'foo'})
        with self.assertRaises(BadCSRFToken):
            self.view(None, request)

    def test_view_with_get_request(self):
        request = self._makeRequest(self.config)
        request.method = 'GET'
        response = self.view(None, request)
        self.assertIsInstance(response, Response)

    def test_view_with_empty_request(self):
        request = self._makeRequest(self.config)
        request.method = 'POST'
        request.POST = {}
        request.headers = {}
        request.session = DummySession({'csrf_token': 'foo'})
        with self.assertRaises(BadCSRFToken):
            self.view(None, request)

class DummySession(dict):
    pass