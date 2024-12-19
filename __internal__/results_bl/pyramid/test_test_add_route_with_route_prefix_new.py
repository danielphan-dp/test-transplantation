import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_without_route_prefix(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        self.assertEqual(config.route_args, ('name',))
        self.assertEqual(config.route_kw, {'path': 'path'})

    def test_add_route_with_empty_name(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(ValueError):
            config.add_route('', 'path')

    def test_add_route_with_none_path(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(TypeError):
            config.add_route('name', None)

    def test_add_route_with_multiple_arguments(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', method='GET', request_method='POST')
        self.assertEqual(config.route_args, ('name', 'path'))
        self.assertEqual(config.route_kw, {'method': 'GET', 'request_method': 'POST'})