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
        self.mapper.connect('route1', 'path1/:param')
        self.mapper.connect('route2', 'path2/:param')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].__class__, Route)
        self.assertEqual(routes[1].__class__, Route)

    def test_get_routes_no_routes(self):
        self.mapper = self._makeOne()
        self.assertEqual(self.mapper.get_routes(), [])

    def test_get_routes_route_with_params(self):
        self.mapper.connect('test_route', 'test/:id')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].pattern, 'test/:id')

    def test_get_routes_route_with_different_methods(self):
        self.mapper.connect('get_route', 'get/:id', request_method='GET')
        self.mapper.connect('post_route', 'post/:id', request_method='POST')
        routes = self.mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].pattern, 'get/:id')
        self.assertEqual(routes[1].pattern, 'post/:id')