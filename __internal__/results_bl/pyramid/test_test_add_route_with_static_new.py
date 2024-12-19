import unittest
from pyramid.config import Configurator

class TestGetRoutes(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_get_routes_empty(self):
        self.assertEqual(self.config.get_routes(), [])

    def test_get_routes_with_static(self):
        self.config.add_route('name', 'path/{foo}', static=True)
        self.assertEqual(len(self.config.get_routes()), 1)
        self.assertEqual(self.config.get_routes()[0].name, 'name')

    def test_get_routes_with_multiple_routes(self):
        self.config.add_route('route1', 'path/{foo}', static=True)
        self.config.add_route('route2', 'path/{bar}', static=True)
        self.assertEqual(len(self.config.get_routes()), 2)

    def test_get_routes_with_dynamic(self):
        self.config.add_route('dynamic_route', 'dynamic/{id}')
        self.assertEqual(len(self.config.get_routes()), 1)
        self.assertEqual(self.config.get_routes()[0].name, 'dynamic_route')

    def test_get_routes_with_conflicting_names(self):
        self.config.add_route('conflict', 'path/{foo}')
        self.config.add_route('conflict', 'path/{bar}')
        self.assertEqual(len(self.config.get_routes()), 2)

if __name__ == '__main__':
    unittest.main()