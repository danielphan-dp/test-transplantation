import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_route_url_with_no_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('home')
        self.assertEqual(result, 'http://example.com:5432/?')

    def test_route_url_with_multiple_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_route_url_with_empty_query_string(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query='')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?')

    def test_route_url_with_special_characters(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query='name=John&Doe')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?name=John&Doe')

    def test_route_url_with_nonexistent_route(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_kwargs(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query='(openlayers)', foo='bar')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?foo=bar&(openlayers)')