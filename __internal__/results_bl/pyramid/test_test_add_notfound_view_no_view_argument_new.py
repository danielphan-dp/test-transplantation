import os
import unittest
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid.interfaces import IRequest
from pyramid.response import Response
from zope.interface import implementedBy

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator(autocommit=True)
        self.config.setup_registry()
        self.config.add_notfound_view()

    def _makeRequest(self):
        from pyramid.request import Request
        return Request(self.config)

    def _getViewCallable(self, exc_iface, request_iface):
        return self.config.get_view(exc_iface, request_iface)

    def test_view_with_http_notfound(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPNotFound), IRequest)
        context = HTTPNotFound()
        result = view(context, request)
        self.assertEqual(result, context)

    def test_view_with_http_forbidden(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPForbidden), IRequest)
        context = HTTPForbidden()
        result = view(context, request)
        self.assertEqual(result, context)

    def test_view_with_invalid_context(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPNotFound), IRequest)
        context = "Invalid Context"
        with self.assertRaises(TypeError):
            view(context, request)

    def test_view_with_none_context(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPNotFound), IRequest)
        context = None
        result = view(context, request)
        self.assertIsNone(result)

    def test_view_with_empty_request(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPNotFound), IRequest)
        context = HTTPNotFound()
        result = view(context, None)
        self.assertEqual(result, context)

    def test_view_with_different_http_exception(self):
        request = self._makeRequest()
        view = self._getViewCallable(implementedBy(HTTPForbidden), IRequest)
        context = HTTPNotFound()
        result = view(context, request)
        self.assertNotEqual(result, context)