import os
import unittest
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from pyramid.interfaces import IRequest
from zope.interface import implementedBy

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator(autocommit=True)
        self.config.setup_registry()
        self.config.add_forbidden_view()

    def _makeRequest(self):
        from pyramid.request import Request
        return Request.blank('/')

    def _getViewCallable(self, exc_iface, request_iface):
        return self.config.get_view_callable(exc_iface, request_iface)

    def test_view_forbidden_response(self):
        request = self._makeRequest()
        view = self._getViewCallable(
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        context = HTTPForbidden()
        result = view(context, request)
        self.assertEqual(result, context)

    def test_view_not_found_response(self):
        request = self._makeRequest()
        view = self._getViewCallable(
            exc_iface=implementedBy(HTTPNotFound),
            request_iface=IRequest,
        )
        context = HTTPNotFound()
        result = view(context, request)
        self.assertEqual(result, context)

    def test_view_with_invalid_context(self):
        request = self._makeRequest()
        view = self._getViewCallable(
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        context = None
        with self.assertRaises(TypeError):
            view(context, request)

    def test_view_with_different_request(self):
        from pyramid.request import Request
        request = Request.blank('/different')
        view = self._getViewCallable(
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        context = HTTPForbidden()
        result = view(context, request)
        self.assertEqual(result, context)