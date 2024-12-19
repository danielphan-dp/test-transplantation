import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_url_with_empty_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', *[])
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_single_element(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', '1')
        self.assertEqual(result, 'http://example.com:5432/1')

    def test_route_url_with_multiple_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', '1', '2', '3')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_query_parameters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', a=1, b=2, c=3)
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1&b=2&c=3')

    def test_route_url_with_invalid_route_name(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_none_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', None)
        self.assertEqual(result, 'http://example.com:5432/None')

    def test_route_url_with_empty_query(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _query={})
        self.assertEqual(result, 'http://example.com:5432/1/2/3')