import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.request import Request

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = Request.blank('/')
        self.request.registry = self.config.registry
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://localhost/1/2/3')

    def test_route_url_with_single_element(self):
        result = self.request.route_url('flub', 'extra1')
        self.assertEqual(result, 'http://localhost/1/2/3/extra1')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'extra1', 'extra2', 'extra3')
        self.assertEqual(result, 'http://localhost/1/2/3/extra1/extra2/extra3')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', 'extra1', 'extra2', param1='value1', param2='value2')
        self.assertEqual(result, 'http://localhost/1/2/3/extra1/extra2?param1=value1&param2=value2')

    def test_route_url_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_route_name(self):
        with self.assertRaises(ValueError):
            self.request.route_url('')

    def test_route_url_with_none_elements(self):
        result = self.request.route_url('flub', None)
        self.assertEqual(result, 'http://localhost/1/2/3/None')