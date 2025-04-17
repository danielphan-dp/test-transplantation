import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', 'https://acme.org/path/{foo}')

    def _makeRequest(self):
        return DummyRequest()

    def test_generate_external_url_with_query(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'foo'}
            return elements, kw

        self.config.add_route('acme', 'https://acme.org/path/{foo}', pregenerator=pregenerator)
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar'),
            'https://acme.org/path/bar?q=foo',
        )

    def test_external_url_with_route_prefix(self):
        def includeme(config):
            config.add_route('acme', '//acme.org/{foo}')

        self.config.include(includeme, route_prefix='some_prefix')
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar'), 'http://acme.org/bar'
        )

    def test_route_url_with_missing_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('acme')

    def test_route_url_with_extra_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar', extra='value'),
            'https://acme.org/path/bar'
        )

    def test_route_url_with_invalid_route(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('invalid_route', foo='bar')