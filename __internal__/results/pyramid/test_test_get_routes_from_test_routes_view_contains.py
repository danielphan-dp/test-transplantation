import unittest
from pyramid.urldispatch import Route

class TestRoutesMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = self._makeOne()

    def _makeOne(self):
        from pyramid.urldispatch import RoutesMapper
        return RoutesMapper()

    def test_get_routes_empty(self):
        self.assertEqual(self.mapper.get_routes(), [])

    def test_get_routes_single_route(self):
        self.mapper.connect('whatever', 'archives/:action/:article')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].__class__, Route)

    def test_get_routes_multiple_routes(self):
        self.mapper.connect('route1', 'path1/:param1')
        self.mapper.connect('route2', 'path2/:param2')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].__class__, Route)
        self.assertEqual(routes[1].__class__, Route)

    def test_get_routes_no_duplicate_routes(self):
        self.mapper.connect('unique_route', 'unique/path')
        self.mapper.connect('unique_route', 'unique/path')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 1)

    def test_get_routes_with_static_route(self):
        self.mapper.add_static('static', '/static/path')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].__class__, Route)

    def test_get_routes_after_removal(self):
        self.mapper.connect('to_remove', 'remove/path')
        self.mapper.get_routes()  # Ensure it is added
        self.mapper.routes.remove(self.mapper.routes[-1])  # Simulate removal
        self.assertEqual(len(self.mapper.get_routes()), 0)