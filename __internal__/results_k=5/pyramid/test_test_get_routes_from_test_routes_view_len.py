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
        self.mapper.connect('route1', 'path/to/resource1')
        self.mapper.connect('route2', 'path/to/resource2')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].__class__, Route)
        self.assertEqual(routes[1].__class__, Route)

    def test_get_routes_no_duplicate_routes(self):
        self.mapper.connect('unique_route', 'path/to/resource')
        self.mapper.connect('unique_route', 'path/to/resource')  # Duplicate
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 1)

    def test_get_routes_with_different_methods(self):
        self.mapper.connect('get_route', 'path/to/get', request_method='GET')
        self.mapper.connect('post_route', 'path/to/post', request_method='POST')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].__class__, Route)
        self.assertEqual(routes[1].__class__, Route)

    def test_get_routes_with_static_route(self):
        self.mapper.add_static('static', '/static/path')
        routes = self.mapper.get_routes()
        self.assertGreater(len(routes), 0)
        self.assertTrue(any(isinstance(route, Route) for route in routes))

if __name__ == '__main__':
    unittest.main()