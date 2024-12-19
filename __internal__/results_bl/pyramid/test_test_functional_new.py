import unittest
from pyramid.exceptions import ConfigurationConflictError
from pyramid.config import Configurator
from pyramid.interfaces import IRoutesMapper

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_args(self):
        self.config.add_route('bar', '/bar')
        self.config.commit()
        mapper = self.config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].name, 'bar')
        self.assertEqual(routes[0].path, '/bar')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationConflictError):
            self.config.add_route('', '/empty')
            self.config.commit()

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('baz', '/baz')
        with self.assertRaises(ConfigurationConflictError):
            self.config.add_route('baz', '/another_baz')
            self.config.commit()

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ConfigurationConflictError):
            self.config.add_route('invalid', None)
            self.config.commit()

    def test_add_route_with_special_characters(self):
        self.config.add_route('foo@bar', '/foo@bar')
        self.config.commit()
        mapper = self.config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].name, 'foo@bar')
        self.assertEqual(routes[0].path, '/foo@bar')

    def test_add_route_with_multiple_args(self):
        self.config.add_route('multi', '/multi', request_method='GET', request_param='param')
        self.config.commit()
        mapper = self.config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].name, 'multi')
        self.assertEqual(routes[0].path, '/multi')
        self.assertEqual(routes[0].request_method, 'GET')
        self.assertEqual(routes[0].request_param, 'param')