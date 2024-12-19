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
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_single_element(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra1')
        self.assertEqual(result, 'http://example.com:5432/1/extra1')

    def test_route_url_with_query_parameters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra1', 'extra2', param1='value1', param2='value2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2?param1=value1&param2=value2')

    def test_route_url_with_empty_route_name(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(ValueError):
            request.route_url('')

    def test_route_url_with_invalid_route_name(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_special_characters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra@1', 'extra#2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra@1/extra#2')