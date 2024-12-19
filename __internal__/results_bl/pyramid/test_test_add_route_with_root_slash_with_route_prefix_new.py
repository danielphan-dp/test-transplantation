import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_with_valid_name_and_path(self):
        config = self._makeOne(autocommit=True)
        config.add_route('test_name', '/test_path')
        self.assertEqual(config.route_args, ('test_name', '/test_path'))
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_empty_name(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(ValueError):
            config.add_route('', '/test_path')

    def test_add_route_with_none_name(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(ValueError):
            config.add_route(None, '/test_path')

    def test_add_route_with_multiple_arguments(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', '/path', request_method='GET', custom_param='value')
        self.assertEqual(config.route_args, ('name', '/path'))
        self.assertEqual(config.route_kw, {'request_method': 'GET', 'custom_param': 'value'})

    def test_add_route_with_root_slash_without_route_prefix(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', '/')
        self.assertEqual(config.route_args, ('name', '/'))
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_root_slash_with_empty_prefix(self):
        config = self._makeOne(autocommit=True)
        config.route_prefix = ''
        config.add_route('name', '/')
        self.assertEqual(config.route_args, ('name', '/'))
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_special_characters_in_name(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name_with_special_chars!@#$', '/path')
        self.assertEqual(config.route_args, ('name_with_special_chars!@#$', '/path'))
        self.assertEqual(config.route_kw, {})