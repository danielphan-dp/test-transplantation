import os
import unittest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.interfaces import IRequest
from pyramid.renderers import null_renderer
from pyramid.response import Response

class TestViews(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        from pyramid.config import Configurator
        return Configurator(autocommit=autocommit)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/', environ={'REQUEST_METHOD': 'GET'})

    def _getViewCallable(self, config, exc_iface, request_iface):
        from pyramid.view import view_config
        return config.get_view(exc_iface, request_iface)

    def test_add_forbidden_view_with_different_renderer(self):
        config = self._makeOne(autocommit=True)
        view = lambda *arg: 'FORBIDDEN'
        config.add_forbidden_view(view, renderer='json')
        request = self._makeRequest(config)
        view = self._getViewCallable(
            config,
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        result = view(None, request)
        self.assertEqual(result, 'FORBIDDEN')

    def test_add_forbidden_view_with_no_renderer(self):
        config = self._makeOne(autocommit=True)
        view = lambda *arg: 'NO RENDERER'
        config.add_forbidden_view(view)
        request = self._makeRequest(config)
        view = self._getViewCallable(
            config,
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        result = view(None, request)
        self.assertEqual(result, 'NO RENDERER')

    def test_add_forbidden_view_with_invalid_request(self):
        config = self._makeOne(autocommit=True)
        view = lambda *arg: 'INVALID REQUEST'
        config.add_forbidden_view(view, renderer=null_renderer)
        request = self._makeRequest(config)
        request.method = 'POST'  # Simulating an invalid request method
        view = self._getViewCallable(
            config,
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        result = view(None, request)
        self.assertEqual(result, 'INVALID REQUEST')

    def test_add_forbidden_view_with_context(self):
        config = self._makeOne(autocommit=True)
        view = lambda context, request: f'FORBIDDEN: {context}'
        config.add_forbidden_view(view, renderer=null_renderer)
        request = self._makeRequest(config)
        view = self._getViewCallable(
            config,
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        result = view('test_context', request)
        self.assertEqual(result, 'FORBIDDEN: test_context')