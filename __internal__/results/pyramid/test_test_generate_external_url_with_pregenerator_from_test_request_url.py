import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('test_route', 'http://example.com/{foo}/{bar}')

    def test_route_url_with_valid_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('test_route', foo='1', bar='2'),
            'http://example.com/1/2'
        )

    def test_route_url_with_missing_elements(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('test_route', foo='1')

    def test_route_url_with_extra_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('test_route', '1', '2', 'extra'),
            'http://example.com/1/2'
        )

    def test_route_url_with_query_parameters(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'test'}
            return elements, kw

        self.config.add_route('query_route', 'http://example.com/path/{foo}', pregenerator=pregenerator)
        request = self.config
        self.assertEqual(
            request.route_url('query_route', foo='bar'),
            'http://example.com/path/bar?q=test'
        )

    def test_route_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route', foo='1', bar='2')