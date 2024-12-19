import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_arguments(self):
        self.config.add_route('name', 'path', accept='text/html')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {'accept': 'text/html'})

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', 'path')

    def test_add_route_with_none_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('name', None)

    def test_add_route_with_invalid_accept_type(self):
        with self.assertRaises(ValueError):
            self.config.add_route('name', 'path', accept='invalid/type')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'path', accept='text/plain', method='GET')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {'accept': 'text/plain', 'method': 'GET'})