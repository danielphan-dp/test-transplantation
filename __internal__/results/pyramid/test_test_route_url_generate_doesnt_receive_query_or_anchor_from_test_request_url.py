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

    def test_route_url_with_query(self):
        result = self.request.route_url('flub', _query={'name': 'some_name'})
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432?name=some_name')

    def test_route_url_with_anchor(self):
        result = self.request.route_url('flub', _anchor='section1')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432#section1')

    def test_route_url_with_elements_and_query(self):
        result = self.request.route_url('flub', 'element1', _query={'name': 'some_name'})
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432/element1?name=some_name')

    def test_route_url_with_elements_and_anchor(self):
        result = self.request.route_url('flub', 'element1', _anchor='section1')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432/element1#section1')

    def test_route_url_with_all_parameters(self):
        result = self.request.route_url('flub', 'element1', _query={'name': 'some_name'}, _anchor='section1')
        self.assertEqual(self.route.kw, {})
        self.assertEqual(result, 'http://example.com:5432/element1?name=some_name#section1')

class DummyRoute:
    def __init__(self, result):
        self.result = result
        self.kw = {}

    def generate(self, kw):
        self.kw = kw
        return self.result

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

if __name__ == '__main__':
    unittest.main()