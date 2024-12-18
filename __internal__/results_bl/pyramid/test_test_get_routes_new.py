import unittest
from pyramid.urldispatch import Route

class TestRoutesMapper(unittest.TestCase):

    def _makeOne(self):
        from pyramid.urldispatch import RoutesMapper
        return RoutesMapper()

    def test_get_routes_empty(self):
        mapper = self._makeOne()
        self.assertEqual(mapper.get_routes(), [])

    def test_get_routes_single_route(self):
        mapper = self._makeOne()
        mapper.connect('whatever', 'archives/:action/:article')
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].__class__, Route)

    def test_get_routes_multiple_routes(self):
        mapper = self._makeOne()
        mapper.connect('route1', 'path1/:param1')
        mapper.connect('route2', 'path2/:param2')
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].__class__, Route)
        self.assertEqual(routes[1].__class__, Route)

    def test_get_routes_no_routes(self):
        mapper = self._makeOne()
        self.assertEqual(mapper.get_routes(), [])

    def test_get_routes_after_disconnect(self):
        mapper = self._makeOne()
        route = mapper.connect('test', 'path/:param')
        mapper.disconnect(route)
        self.assertEqual(mapper.get_routes(), [])

    def test_get_routes_with_different_patterns(self):
        mapper = self._makeOne()
        mapper.connect('route1', 'path1/:param1')
        mapper.connect('route2', 'path2/:param2')
        mapper.connect('route3', 'path3/:param3')
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 3)
        self.assertTrue(all(isinstance(route, Route) for route in routes))