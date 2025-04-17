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

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_route_url_with_anchor(self):
        result = self.request.route_url('flub', _anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_route_url_with_unicode_anchor(self):
        result = self.request.route_url('flub', _anchor='La Pe\xc3\xb1a')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#La%20Pe%C3%B1a')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', 'element@#$', _anchor='test&anchor')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element%40%23%24#test%26anchor')