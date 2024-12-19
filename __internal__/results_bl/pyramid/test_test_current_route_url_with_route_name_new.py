import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.util import text_

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
        result = request.current_route_url('extra1', 'extra2', _query={})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_current_route_url_with_invalid_route_name(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('extra1', 'extra2', _route_name='invalid')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_current_route_url_with_special_characters(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('extra@1', 'extra#2', _query={'a': 1})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra%401/extra%232?a=1')

    def test_current_route_url_with_anchor(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url('extra1', 'extra2', _anchor=text_(b"foo"))
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2#foo')