import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.util import text_
from pyramid.url import current_route_url

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

    def test_current_route_url_with_single_element(self):
        result = self.request.current_route_url('element1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1')

    def test_current_route_url_with_multiple_elements(self):
        result = self.request.current_route_url('element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_current_route_url_with_query_parameters(self):
        result = self.request.current_route_url(_query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param1=value1&param2=value2')

    def test_current_route_url_with_anchor(self):
        result = self.request.current_route_url(_anchor=text_(b"section1"))
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_current_route_url_with_elements_and_query(self):
        result = self.request.current_route_url('element1', _query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1?param=value')

    def test_current_route_url_with_elements_and_anchor(self):
        result = self.request.current_route_url('element1', _anchor=text_(b"section2"))
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1#section2')

    def test_current_route_url_with_all_parameters(self):
        result = self.request.current_route_url('element1', 'element2', _query={'a': 1}, _anchor=text_(b"foo"))
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2?a=1#foo')