import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class TestCurrentRoutePath(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.route = DummyRoute('/1/2/3')
        self.mapper = DummyRoutesMapper(route=self.route)
        self.request.matched_route = self.route
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_current_route_path_with_extra_elements(self):
        result = self.request.current_route_path('extra1', 'extra2', _query={'a': 1}, _anchor='foo')
        self.assertEqual(result, '/1/2/3/extra1/extra2?a=1#foo')

    def test_current_route_path_with_no_elements(self):
        result = self.request.current_route_path()
        self.assertEqual(result, '/1/2/3')

    def test_current_route_path_with_only_query(self):
        result = self.request.current_route_path(_query={'b': 2})
        self.assertEqual(result, '/1/2/3?_query=b=2')

    def test_current_route_path_with_only_anchor(self):
        result = self.request.current_route_path(_anchor='bar')
        self.assertEqual(result, '/1/2/3#bar')

    def test_current_route_path_with_empty_query_and_anchor(self):
        result = self.request.current_route_path(_query={}, _anchor='')
        self.assertEqual(result, '/1/2/3')

    def test_current_route_path_with_invalid_route(self):
        self.request.matched_route = None
        result = self.request.current_route_path('extra1')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()