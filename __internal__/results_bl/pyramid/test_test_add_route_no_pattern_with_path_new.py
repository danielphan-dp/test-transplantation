import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def _assertRoute(self, config, name, path):
        route = config.registry.routes.get(name)
        self.assertIsNotNone(route)
        self.assertEqual(route.pattern, path)

    def test_add_route_with_only_name(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name_only')
        self.assertIn('name_only', config.registry.routes)

    def test_add_route_with_empty_path(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name_empty', path='')
        self._assertRoute(config, 'name_empty', '')

    def test_add_route_with_none_path(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(TypeError):
            config.add_route('name_none', path=None)

    def test_add_route_with_multiple_arguments(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name_multi', 'path1', 'path2')
        self.assertIn('name_multi', config.registry.routes)

    def test_add_route_with_keyword_arguments(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name_kw', path='path', request_method='GET')
        self._assertRoute(config, 'name_kw', 'path')