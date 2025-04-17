import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', '//acme.org/{foo}')

    def _makeRequest(self):
        return DummyRequest()

    def test_route_url_with_valid_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(request.route_url('acme', foo='bar'), 'http://acme.org/bar')

    def test_route_url_with_missing_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('acme')

    def test_route_url_with_extra_elements(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(request.route_url('acme', 'extra', foo='bar'), 'http://acme.org/bar/extra')

    def test_route_url_with_query_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(request.route_url('acme', foo='bar', _query={'key': 'value'}), 'http://acme.org/bar?key=value')

    def test_route_url_with_route_prefix(self):
        self.config.include(lambda config: config.add_route('acme', '//acme.org/{foo}'), route_prefix='some_prefix')
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(request.route_url('acme', foo='bar'), 'http://acme.org/bar')