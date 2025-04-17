import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_no_arguments(self):
        self.config.add_route('empty_route')
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_only_name(self):
        self.config.add_route('test_route')
        self.assertEqual(self.config.route_args, ('test_route',))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_path(self):
        self.config.add_route('test_route', '/test')
        self.assertEqual(self.config.route_args, ('test_route', '/test'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('test_route', '/test', request_method='GET')
        self.assertEqual(self.config.route_args, ('test_route', '/test'))
        self.assertEqual(self.config.route_kw, {'request_method': 'GET'})

    def test_add_route_with_invalid_method(self):
        with self.assertRaises(ValueError):
            self.config.add_route('test_route', '/test', request_method='INVALID_METHOD')

    def test_add_route_with_path_info(self):
        self.config.add_route('path_info_route', '/path/{param}')
        self.assertEqual(self.config.route_args, ('path_info_route', '/path/{param}'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('empty_path_route', '')

if __name__ == '__main__':
    unittest.main()