import unittest
from pyramid.config import Configurator
from pyramid.request import Request

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_with_valid_name_and_path(self):
        self.config.add_route('test_route', '/test/{param}')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'test_route')
        self.assertEqual(route[0].pattern, '/test/{param}')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/test/{param}')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('test_route', '')

    def test_add_route_with_multiple_parameters(self):
        self.config.add_route('multi_param_route', '/test/{param1}/{param2}')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'multi_param_route')
        self.assertEqual(route[0].pattern, '/test/{param1}/{param2}')

    def test_add_route_with_query_params(self):
        self.config.add_route('query_param_route', '/test')
        request = Request.blank('/test?param=value')
        self.assertEqual(request.params['param'], 'value')

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_char_route', '/test/{param}')
        request = Request.blank('/test/!@#$%^&*()')
        self.assertEqual(request.path_info, '/test/!@#$%^&*()')

    def test_add_route_with_nonexistent_route(self):
        self.assertIsNone(self.config.get_route('nonexistent_route'))

if __name__ == '__main__':
    unittest.main()