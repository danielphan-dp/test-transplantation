import unittest
from pyramid.config import Configurator

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
        self.config.add_route('duplicate_route', '/second/path')
        routes = self.config.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].pattern, '/second/path')

    def test_add_route_with_pregenerator(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'test'}
            return elements, kw

        self.config.add_route('test_route', '/test/{foo}', pregenerator=pregenerator)
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('test_route', foo='bar'),
            '/test/bar?q=test'
        )

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid_route', '')

    def _makeRequest(self):
        from pyramid.request import Request
        from pyramid.testing import DummyRequest
        return DummyRequest()

if __name__ == '__main__':
    unittest.main()