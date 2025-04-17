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
            request.route_url('test_route', foo='value1', bar='value2'),
            'http://example.com/value1/value2'
        )

    def test_route_url_with_missing_elements(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('test_route', foo='value1')

    def test_route_url_with_extra_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('test_route', 'value1', 'value2', 'extra'),
            'http://example.com/value1/value2'
        )

    def test_route_url_with_query_parameters(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'test'}
            return elements, kw

        self.config.add_route('acme', 'https://acme.org/path/{foo}', pregenerator=pregenerator)
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar'),
            'https://acme.org/path/bar?q=test'
        )

    def test_route_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route', foo='value1', bar='value2')