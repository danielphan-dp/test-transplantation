import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.interfaces import IRequest
from pyramid.renderers import null_renderer
from pyramid.response import Response

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator(autocommit=True)

    def test_view_with_none_context(self):
        view = lambda context, request: (context, request)
        request = self._makeRequest(self.config)
        result = view(None, request)
        self.assertEqual(result, (None, request))

    def test_view_with_empty_context(self):
        view = lambda context, request: (context, request)
        request = self._makeRequest(self.config)
        result = view({}, request)
        self.assertEqual(result, ({}, request))

    def test_view_with_valid_context(self):
        view = lambda context, request: (context, request)
        request = self._makeRequest(self.config)
        result = view({'key': 'value'}, request)
        self.assertEqual(result, ({'key': 'value'}, request))

    def test_view_with_invalid_request(self):
        view = lambda context, request: (context, request)
        invalid_request = None
        with self.assertRaises(TypeError):
            view({}, invalid_request)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/', environ={'REQUEST_METHOD': 'GET'})

    def test_view_with_http_not_found(self):
        view = lambda context, request: (context, request)
        request = self._makeRequest(self.config)
        result = view(HTTPNotFound(), request)
        self.assertEqual(result, (HTTPNotFound(), request))