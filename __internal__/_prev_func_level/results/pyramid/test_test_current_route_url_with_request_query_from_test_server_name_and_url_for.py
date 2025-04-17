import os
import unittest
from webob.multidict import GetDict
from pyramid.interfaces import IRoutesMapper

class TestCurrentRouteUrl(unittest.TestCase):
    def _makeOne(self):
        from pyramid.request import Request
        return Request()

    def test_current_route_url_with_empty_query(self):
        request = self._makeOne()
        request.GET = GetDict([], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_special_characters(self):
        request = self._makeOne()
        request.GET = GetDict([('q', 'hello world!')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?q=hello%20world%21')

    def test_current_route_url_with_multiple_routes(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123')], {})
        route1 = DummyRoute('/1/2/3')
        route2 = DummyRoute('/4/5/6')
        mapper = DummyRoutesMapper(route=route1)
        request.matched_route = route2
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/4/5/6?q=123')

    def test_current_route_url_with_no_route(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123')], {})
        request.matched_route = None
        request.matchdict = {}
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/?q=123')

    def test_current_route_url_with_query_string(self):
        request = self._makeOne()
        request.GET = GetDict([('key', 'value')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'extra': 'data'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?extra=data')