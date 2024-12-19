import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.util import text_
from pyramid.url import route_url

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2', a=1, b=2)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2?a=1&b=2')

    def test_route_url_with_empty_elements(self):
        result = self.request.route_url('flub', '', a=1)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/?a=1')

    def test_route_url_with_no_query_params(self):
        result = self.request.route_url('flub', 'element1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', 'element@#$', _query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element@#$?param=value')

    def test_route_url_with_anchor(self):
        result = self.request.route_url('flub', _anchor=text_(b"foo"))
        self.assertEqual(result, 'http://example.com:5432/1/2/3#foo')

    def test_route_url_with_multiple_query_params(self):
        result = self.request.route_url('flub', a=1, b=2, c=3)
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1&b=2&c=3')

    def test_route_url_with_nonexistent_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

if __name__ == '__main__':
    unittest.main()