import os
import unittest
from pyramid.httpexceptions import HTTPNotFound, HTTPMovedPermanently
from pyramid.interfaces import IRequest
from pyramid.renderers import null_renderer
from pyramid.response import Response
from zope.interface import implementedBy

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator(autocommit=True)
        self.config.add_route('foo', '/foo/')

    def test_view_with_valid_request(self):
        request = self._makeRequest()
        request.path_info = '/foo'
        request.query_string = 'a=1&b=2'
        request.path = '/scriptname/foo'
        
        view = self._getViewCallable(request)
        result = view(None, request)
        
        self.assertIsInstance(result, HTTPMovedPermanently)
        self.assertEqual(result.location, '/scriptname/foo/?a=1&b=2')

    def test_view_with_invalid_request(self):
        request = self._makeRequest()
        request.path_info = '/invalid'
        
        view = self._getViewCallable(request)
        result = view(None, request)
        
        self.assertIsInstance(result, HTTPNotFound)

    def test_view_with_no_query_string(self):
        request = self._makeRequest()
        request.path_info = '/foo'
        request.path = '/scriptname/foo'
        
        view = self._getViewCallable(request)
        result = view(None, request)
        
        self.assertIsInstance(result, HTTPMovedPermanently)
        self.assertEqual(result.location, '/scriptname/foo/')

    def _makeRequest(self):
        from pyramid.request import Request
        return Request(self.config)

    def _getViewCallable(self, request):
        return self.config.get_view(request)

if __name__ == '__main__':
    unittest.main()