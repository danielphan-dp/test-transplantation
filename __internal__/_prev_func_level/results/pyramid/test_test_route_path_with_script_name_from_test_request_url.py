import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_path_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub')
        self.assertEqual(result, '/1/2/3')

    def test_route_path_with_empty_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', '')
        self.assertEqual(result, '/1/2/3/')

    def test_route_path_with_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra1', 'extra2', a=1, b=2)
        self.assertEqual(result, '/1/2/3/extra1/extra2?a=1&b=2')

    def test_route_path_with_anchor(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra1', 'extra2', _anchor='foo')
        self.assertEqual(result, '/1/2/3/extra1/extra2#foo')

    def test_route_path_with_script_name(self):
        request = self._makeOne()
        request.script_name = '/foo'
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra1', 'extra2', a=1, b=2, _query={'a': 1}, _anchor='foo')
        self.assertEqual(result, '/foo/1/2/3/extra1/extra2?a=1#foo')

    def test_route_path_with_nonexistent_route(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=None)
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(Exception):
            request.route_path('nonexistent_route')

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result