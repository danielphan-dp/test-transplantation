import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_path_without_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub')
        self.assertEqual(result, '/1')

    def test_route_path_with_empty_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', '')
        self.assertEqual(result, '/1/2/3/?')

    def test_route_path_with_no_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra1', 'extra2')
        self.assertEqual(result, '/1/2/3/extra1/extra2')

    def test_route_path_with_invalid_route_name(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_path('invalid_route')

    def test_route_path_with_special_characters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra@1', 'extra#2')
        self.assertEqual(result, '/1/2/3/extra@1/extra#2')

    def test_route_path_with_multiple_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'extra1', 'extra2', a=1, b=2)
        self.assertEqual(result, '/1/2/3/extra1/extra2?a=1&b=2')