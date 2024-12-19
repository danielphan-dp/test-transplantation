import unittest
import warnings
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_with_no_arguments(self):
        config = self._makeOne()
        config.add_route()
        self.assertEqual(config.route_args, ())
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_only_name(self):
        config = self._makeOne()
        config.add_route('foo')
        self.assertEqual(config.route_args, ('foo',))
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_name_and_path(self):
        config = self._makeOne()
        config.add_route('foo', '/bar')
        self.assertEqual(config.route_args, ('foo', '/bar'))
        self.assertEqual(config.route_kw, {})

    def test_add_route_with_effective_principals(self):
        config = self._makeOne(autocommit=True)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always', DeprecationWarning)
            config.add_route('foo', '/bar', effective_principals=['any'])
            self.assertIn('deprecated effective_principals', str(w[-1].message))

    def test_add_route_with_invalid_effective_principals(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(TypeError):
            config.add_route('foo', '/bar', effective_principals='invalid')

    def test_add_route_with_multiple_arguments(self):
        config = self._makeOne()
        config.add_route('foo', '/bar', request_method='GET', name='test_route')
        self.assertEqual(config.route_args, ('foo', '/bar'))
        self.assertEqual(config.route_kw, {'request_method': 'GET', 'name': 'test_route'})