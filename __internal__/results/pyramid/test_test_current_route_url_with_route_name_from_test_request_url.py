import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from webob.multidict import GetDict

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

    def test_current_route_url_with_empty_query(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={})
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_multiple_elements(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('extra1', 'extra2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_current_route_url_with_query_and_elements(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('extra1', 'extra2', _query={'a': 1})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2?a=1')

    def test_current_route_url_with_query_override(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'a': 1})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1')

    def test_current_route_url_with_duplicate_query_entries(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123'), ('b', '2'), ('b', '2'), ('q', '456')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?q=123&b=2&b=2&q=456')