import os
import unittest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.interfaces import IRequest
from pyramid.response import Response
from pyramid.testing import DummyRequest

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator(autocommit=True)
        self.request = DummyRequest()

    def test_view_forbidden_response(self):
        view = lambda context, request: Response(status=403)
        self.config.add_forbidden_view(view, renderer='json')
        view_callable = self.config.get_view_callable(
            exc_iface=implementedBy(HTTPForbidden),
            request_iface=IRequest,
        )
        result = view_callable(None, self.request)
        self.assertEqual(result.status, '403 Forbidden')

    def test_view_empty_context(self):
        view = lambda context, request: Response(json={'message': 'No context'})
        self.config.add_view(view, context=None, renderer='json')
        view_callable = self.config.get_view_callable(
            context=None,
            request_iface=IRequest,
        )
        result = view_callable(None, self.request)
        self.assertEqual(result.json, {'message': 'No context'})

    def test_view_with_invalid_request(self):
        view = lambda context, request: Response(status=400)
        self.config.add_view(view, context=None, renderer='json')
        view_callable = self.config.get_view_callable(
            context=None,
            request_iface=IRequest,
        )
        invalid_request = DummyRequest(method='INVALID')
        result = view_callable(None, invalid_request)
        self.assertEqual(result.status, '400 Bad Request')

    def test_view_with_renderer(self):
        view = lambda context, request: Response(json={'data': 'test'})
        self.config.add_view(view, renderer='json')
        view_callable = self.config.get_view_callable(
            context=None,
            request_iface=IRequest,
        )
        result = view_callable(None, self.request)
        self.assertEqual(result.json, {'data': 'test'})