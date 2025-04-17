import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', '//acme.org/path/{foo}')

    def _makeRequest(self):
        return DummyRequest()

    def test_generate_external_url_with_valid_foo(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar'), 'http://acme.org/path/bar'
        )

    def test_generate_external_url_with_missing_foo(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('acme')

    def test_generate_external_url_with_invalid_route(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('nonexistent_route', foo='bar')

    def test_generate_external_url_with_multiple_elements(self):
        self.config.add_route('multi', '//example.com/{foo}/{bar}')
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('multi', 'value1', 'value2'), 'http://example.com/value1/value2'
        )

    def test_generate_external_url_with_query_params(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'test'}
            return elements, kw

        self.config.add_route('acme_with_query', 'https://acme.org/path/{foo}', pregenerator=pregenerator)
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme_with_query', foo='bar'), 'https://acme.org/path/bar?q=test'
        )