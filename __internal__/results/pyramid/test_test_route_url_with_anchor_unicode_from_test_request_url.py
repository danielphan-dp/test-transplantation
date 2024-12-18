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
        result = self.request.route_url('flub', 'extra1', 'extra2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_route_url_with_anchor(self):
        anchor = 'section1'
        result = self.request.route_url('flub', _anchor=anchor)
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_route_url_with_unicode_anchor(self):
        anchor = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = self.request.route_url('flub', _anchor=anchor)
        self.assertEqual(result, 'http://example.com:5432/1/2/3#La%20Pe%C3%B1a')

    def test_route_url_with_nonexistent_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_invalid_elements(self):
        with self.assertRaises(TypeError):
            self.request.route_url('flub', 123)

if __name__ == '__main__':
    unittest.main()