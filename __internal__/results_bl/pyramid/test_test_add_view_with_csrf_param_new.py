import os
import unittest
from pyramid.renderers import null_renderer
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken

class TestView(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        from pyramid.config import Configurator
        return Configurator(autocommit=autocommit)

    def _getViewCallable(self, config):
        return config.make_wsgi_app()

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/', environ={'REQUEST_METHOD': 'POST'})

    def test_view_with_invalid_csrf_token(self):
        def view(request):
            return 'OK'

        config = self._makeOne(autocommit=True)
        config.add_view(view, require_csrf='st', renderer=null_renderer)
        view = self._getViewCallable(config)
        request = self._makeRequest(config)
        request.scheme = "http"
        request.method = 'POST'
        request.POST = {'st': 'foo'}
        request.headers = {}
        request.session = DummySession({'csrf_token': 'invalid_token'})
        
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_view_with_missing_csrf_param(self):
        def view(request):
            return 'OK'

        config = self._makeOne(autocommit=True)
        config.add_view(view, require_csrf='st', renderer=null_renderer)
        view = self._getViewCallable(config)
        request = self._makeRequest(config)
        request.scheme = "http"
        request.method = 'POST'
        request.POST = {}
        request.headers = {}
        request.session = DummySession({'csrf_token': 'foo'})
        
        with self.assertRaises(BadCSRFToken):
            view(None, request)

    def test_view_with_get_method(self):
        def view(request):
            return 'OK'

        config = self._makeOne(autocommit=True)
        config.add_view(view, require_csrf='st', renderer=null_renderer)
        view = self._getViewCallable(config)
        request = self._makeRequest(config)
        request.scheme = "http"
        request.method = 'GET'
        request.POST = {}
        request.headers = {}
        request.session = DummySession({'csrf_token': 'foo'})
        
        self.assertEqual(view(None, request), 'OK')

class DummySession:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        return self.data[key]