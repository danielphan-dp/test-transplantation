import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_no_arguments(self):
        self.config.add_route('empty_route')
        self.assertEqual(self.config.routes['empty_route'].name, 'empty_route')

    def test_add_route_with_only_name(self):
        self.config.add_route('test_route')
        self.assertEqual(self.config.routes['test_route'].name, 'test_route')

    def test_add_route_with_path(self):
        self.config.add_route('path_route', '/path')
        self.assertEqual(self.config.routes['path_route'].pattern, '/path')

    def test_add_route_with_invalid_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/path')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('multi_arg_route', '/multi/{foo}', request_method='GET')
        route = self.config.routes['multi_arg_route']
        self.assertEqual(route.pattern, '/multi/{foo}')
        self.assertEqual(route.request_method, ('GET',))

    def test_add_route_with_keyword_arguments(self):
        self.config.add_route('kwarg_route', '/kwarg', request_param='abc')
        route = self.config.routes['kwarg_route']
        self.assertEqual(route.request_param, 'abc')

    def test_add_route_with_path_info(self):
        self.config.add_route('path_info_route', '/path_info', path_info='/path_info')
        route = self.config.routes['path_info_route']
        self.assertEqual(route.path_info, '/path_info')

    def test_add_route_with_conflicting_name(self):
        self.config.add_route('conflict_route', '/conflict')
        with self.assertRaises(KeyError):
            self.config.add_route('conflict_route', '/new_conflict')

if __name__ == '__main__':
    unittest.main()