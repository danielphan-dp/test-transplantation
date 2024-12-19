import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from webob.multidict import GetDict

class TestCurrentRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.route = DummyRoute('/1/2/3')
        self.mapper = DummyRoutesMapper(route=self.route)
        self.request.matched_route = self.route
        self.request.matchdict = {}
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_current_route_url_with_no_elements(self):
        result = self.request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_additional_elements(self):
        result = self.request.current_route_url('extra', 'params')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra/params')

    def test_current_route_url_with_query_params(self):
        self.request.GET = GetDict([('q', '456')], {})
        result = self.request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?q=456')

    def test_current_route_url_with_empty_query_params(self):
        self.request.GET = GetDict([], {})
        result = self.request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_kw_arguments(self):
        result = self.request.current_route_url(foo='bar')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?foo=bar')

    def test_current_route_url_with_multiple_kw_arguments(self):
        result = self.request.current_route_url(foo='bar', baz='qux')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?foo=bar&baz=qux')

    def test_current_route_url_with_no_route(self):
        self.request.matched_route = None
        result = self.request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/')