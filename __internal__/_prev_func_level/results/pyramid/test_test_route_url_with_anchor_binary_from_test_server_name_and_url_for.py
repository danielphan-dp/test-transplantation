import unittest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.request = self._makeOne()
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

    def test_route_url_with_anchor_string(self):
        result = self.request.route_url('flub', _anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#section1')

    def test_route_url_with_anchor_binary(self):
        result = self.request.route_url('flub', _anchor=b"La Pe\xc3\xb1a")
        self.assertEqual(result, 'http://example.com:5432/1/2/3#La%20Pe%C3%B1a')

    def test_route_url_with_nonexistent_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('nonexistent_route')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', _anchor='!@#$%^&*()')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#!%40%23%24%25%5E%26%2A%28%29')

    def _makeOne(self):
        from pyramid.request import Request
        return Request.blank('/')

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result