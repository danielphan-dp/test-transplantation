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

    def test_route_url_with_unicode_elements(self):
        unicode_element = text_(b'El Ni\xc3\xb1o', 'utf-8')
        result = self.request.route_url('flub', unicode_element)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/El%20Ni%C3%B1o')

    def test_route_url_with_anchor(self):
        anchor = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = self.request.route_url('flub', _anchor=anchor)
        self.assertEqual(result, 'http://example.com:5432/1/2/3#La%20Pe%C3%B1a')

    def test_route_url_with_nonexistent_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_special_characters(self):
        special_element = 'element@#$%'
        result = self.request.route_url('flub', special_element)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element%40%23%24%25')