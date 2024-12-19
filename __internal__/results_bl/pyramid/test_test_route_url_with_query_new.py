import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_route_url_without_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('home')
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_multiple_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', '1', '2', '3')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_empty_query(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={})
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_invalid_route(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/invalid'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_special_characters(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={'q': 'test@123'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?q=test%40123')