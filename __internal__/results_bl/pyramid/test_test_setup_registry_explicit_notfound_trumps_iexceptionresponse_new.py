import os
import unittest
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.registry import Registry
from pyramid.renderers import null_renderer
from pyramid.interfaces import IRequest

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        self.reg = Registry()
        self.config = self._makeOne(self.reg, autocommit=True)
        self.config.setup_registry()

    def _makeOne(self, reg, autocommit=False):
        from pyramid.config import Configurator
        return Configurator(registry=reg, autocommit=autocommit)

    def _makeRequest(self, config):
        from pyramid.testing import DummyRequest
        return DummyRequest()

    def test_view_with_http_notfound(self):
        def myview(context, request):
            return 'Not Found'

        self.config.add_view(myview, context=HTTPNotFound, renderer=null_renderer)
        request = self._makeRequest(self.config)
        view = self.config.get_view(context=HTTPNotFound, request=request)
        result = view(None, request)
        self.assertEqual(result, 'Not Found')

    def test_view_with_http_badrequest(self):
        def myview(context, request):
            return 'Bad Request'

        self.config.add_view(myview, context=HTTPBadRequest, renderer=null_renderer)
        request = self._makeRequest(self.config)
        view = self.config.get_view(context=HTTPBadRequest, request=request)
        result = view(None, request)
        self.assertEqual(result, 'Bad Request')

    def test_view_with_none_context(self):
        def myview(context, request):
            return 'No Context'

        self.config.add_view(myview, context=HTTPNotFound, renderer=null_renderer)
        request = self._makeRequest(self.config)
        view = self.config.get_view(context=HTTPNotFound, request=request)
        result = view(None, request)
        self.assertEqual(result, 'No Context')

    def test_view_with_invalid_context(self):
        def myview(context, request):
            return 'Invalid Context'

        self.config.add_view(myview, context=object, renderer=null_renderer)
        request = self._makeRequest(self.config)
        view = self.config.get_view(context=object, request=request)
        result = view(None, request)
        self.assertEqual(result, 'Invalid Context')

if __name__ == '__main__':
    unittest.main()