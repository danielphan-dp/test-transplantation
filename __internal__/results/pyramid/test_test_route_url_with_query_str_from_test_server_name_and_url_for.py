import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_route_url_with_query_string(self):
        result = self.request.route_url('flub', _query='(openlayers)')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?(openlayers)')

    def test_route_url_with_dynamic_path_elements(self):
        result = self.request.route_url('flub', foo='1', bar='2')
        self.assertEqual(result, 'http://example.com:5432/1/2')

    def test_route_url_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_query_string(self):
        result = self.request.route_url('flub', _query='')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', 'element with spaces', _query='key=value')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element%20with%20spaces?key=value')