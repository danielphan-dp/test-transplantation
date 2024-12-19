import os
import unittest
from pyramid.httpexceptions import HTTPNotFound, HTTPTemporaryRedirect
from pyramid.interfaces import IRequest
from pyramid.renderers import null_renderer
from pyramid.response import Response
from pyramid.config import Configurator

class TestViews(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)
        self.config.add_route('foo', '/foo/')

    def test_view_redirects_with_query_string(self):
        def view(request):  # pragma: no cover
            return Response('OK')

        self.config.add_notfound_view(view, renderer=null_renderer, append_slash=True)
        request = self.config.make_request()
        request.path_info = '/foo'
        request.query_string = 'a=1&b=2'
        request.path = '/scriptname/foo'
        view_callable = self.config.get_view_callable(exc_iface=implementedBy(HTTPNotFound), request_iface=IRequest)
        result = view_callable(None, request)
        self.assertTrue(isinstance(result, HTTPTemporaryRedirect))
        self.assertEqual(result.location, '/scriptname/foo/?a=1&b=2')

    def test_view_redirects_without_query_string(self):
        def view(request):  # pragma: no cover
            return Response('OK')

        self.config.add_notfound_view(view, renderer=null_renderer, append_slash=True)
        request = self.config.make_request()
        request.path_info = '/foo'
        request.path = '/scriptname/foo'
        view_callable = self.config.get_view_callable(exc_iface=implementedBy(HTTPNotFound), request_iface=IRequest)
        result = view_callable(None, request)
        self.assertTrue(isinstance(result, HTTPTemporaryRedirect))
        self.assertEqual(result.location, '/scriptname/foo/')

    def test_view_with_invalid_path(self):
        def view(request):  # pragma: no cover
            return Response('OK')

        self.config.add_notfound_view(view, renderer=null_renderer, append_slash=True)
        request = self.config.make_request()
        request.path_info = '/invalid'
        request.path = '/scriptname/invalid'
        view_callable = self.config.get_view_callable(exc_iface=implementedBy(HTTPNotFound), request_iface=IRequest)
        result = view_callable(None, request)
        self.assertTrue(isinstance(result, HTTPTemporaryRedirect))
        self.assertEqual(result.location, '/scriptname/invalid/')

    def test_view_with_empty_path(self):
        def view(request):  # pragma: no cover
            return Response('OK')

        self.config.add_notfound_view(view, renderer=null_renderer, append_slash=True)
        request = self.config.make_request()
        request.path_info = ''
        request.path = '/scriptname/'
        view_callable = self.config.get_view_callable(exc_iface=implementedBy(HTTPNotFound), request_iface=IRequest)
        result = view_callable(None, request)
        self.assertTrue(isinstance(result, HTTPTemporaryRedirect))
        self.assertEqual(result.location, '/scriptname/?')

if __name__ == '__main__':
    unittest.main()