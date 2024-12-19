import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_url_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub')
        self.assertEqual(result, '/')

    def test_route_url_with_empty_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', '')
        self.assertEqual(result, '/1/2/3')

    def test_route_url_with_multiple_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'a', 'b', 'c')
        self.assertEqual(result, '/1/2/3/a/b/c')

    def test_route_url_with_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, '/1/2/3?key=value')

    def test_route_url_with_invalid_route_name(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_app_url_and_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _app_url='http://example.com')
        self.assertEqual(result, 'http://example.com/1/2/3')