import os
import unittest
from pyramid.testing import DummyRequest, DummyRoute
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_url_with_anchor_None(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _anchor=None)
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_anchor_set(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_route_url_with_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_route_url_with_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param1=value1&param2=value2')

    def test_route_url_with_empty_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', '')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/')

    def test_route_url_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')