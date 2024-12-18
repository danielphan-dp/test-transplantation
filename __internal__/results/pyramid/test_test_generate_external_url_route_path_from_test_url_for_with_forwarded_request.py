import unittest
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_name_and_path(self):
        self.config.add_route('test_route', '/test/path')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'test_route')
        self.assertEqual(route[0].pattern, '/test/path')

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('duplicate_route', '/first/path')
        with self.assertRaises(ConfigurationError):
            self.config.add_route('duplicate_route', '/second/path')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/path')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('invalid_route', None)

    def test_add_route_with_path_info(self):
        self.config.add_route('path_info_route', '/path/{foo}')
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertRaises(ValueError, request.route_path, 'path_info_route', foo='bar')

    def _makeRequest(self):
        from pyramid.request import Request
        from pyramid.testing import DummyRequest
        return DummyRequest()

if __name__ == '__main__':
    unittest.main()