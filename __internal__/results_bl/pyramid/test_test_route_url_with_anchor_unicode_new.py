import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.util import text_
from pyramid.url import route_url

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
        result = self.request.route_url('flub', _query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param1=value1&param2=value2')

    def test_route_url_with_anchor_unicode(self):
        anchor = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = self.request.route_url('flub', _anchor=anchor)
        self.assertEqual(result, 'http://example.com:5432/1/2/3#La%20Pe%C3%B1a')

    def test_route_url_with_nonexistent_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', _anchor='special@char!')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#special%40char%21')

    def test_route_url_with_no_route_name(self):
        with self.assertRaises(TypeError):
            self.request.route_url()

if __name__ == '__main__':
    unittest.main()