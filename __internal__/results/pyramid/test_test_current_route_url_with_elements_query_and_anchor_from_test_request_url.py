import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestCurrentRouteUrl(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_current_route_url_with_no_elements(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_empty_elements(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/')

    def test_current_route_url_with_query_parameters(self):
        from webob.multidict import GetDict
        request = self._makeOne()
        request.GET = GetDict([('param', 'value')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param=value')

    def test_current_route_url_with_multiple_query_parameters(self):
        from webob.multidict import GetDict
        request = self._makeOne()
        request.GET = GetDict([('a', '1'), ('b', '2')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1&b=2')

    def test_current_route_url_with_anchor(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_current_route_url_with_query_and_anchor(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'a': 1}, _anchor='foo')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1#foo')