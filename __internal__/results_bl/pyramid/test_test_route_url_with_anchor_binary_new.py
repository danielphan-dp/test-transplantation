import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_empty_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', _anchor='special&char')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#special%26char')

    def test_route_url_with_non_ascii_anchor(self):
        result = self.request.route_url('flub', _anchor='Café')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#Caf%C3%A9')

    def test_route_url_with_no_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_numeric_elements(self):
        result = self.request.route_url('flub', 123, 456)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/123/456')