import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.route = DummyRoute(result='http://example.com:5432')
        self.mapper = DummyRoutesMapper(route=self.route)
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements_or_kw(self):
        result = self.request.route_url('flub')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432')

    def test_route_url_with_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432/element1/element2')

    def test_route_url_with_kw_arguments(self):
        result = self.request.route_url('flub', foo='bar')
        self.assertEqual(self.route.kw, {'foo': 'bar'})
        self.assertEqual(result, 'http://example.com:5432?foo=bar')

    def test_route_url_with_multiple_kw_arguments(self):
        result = self.request.route_url('flub', foo='bar', baz='qux')
        self.assertEqual(self.route.kw, {'foo': 'bar', 'baz': 'qux'})
        self.assertEqual(result, 'http://example.com:5432?foo=bar&baz=qux')

    def test_route_url_with_empty_query(self):
        result = self.request.route_url('flub', _query={})
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432')

    def test_route_url_with_anchor(self):
        result = self.request.route_url('flub', _anchor='section1')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432#section1')

    def test_route_url_with_query_and_anchor(self):
        result = self.request.route_url('flub', _query={'name': 'some_name'}, _anchor='section1')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432?name=some_name#section1')

    def test_route_url_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

if __name__ == '__main__':
    unittest.main()