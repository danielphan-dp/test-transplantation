import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_parameters(self):
        self.config.add_route('test_route', '/test/{param}')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'test_route')
        self.assertEqual(route[0].pattern, '/test/{param}')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/test/{param}')

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('test_route', '')

    def test_add_route_with_multiple_routes(self):
        self.config.add_route('route_one', '/one')
        self.config.add_route('route_two', '/two')
        routes = self.config.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertIn('route_one', [route.name for route in routes])
        self.assertIn('route_two', [route.name for route in routes])

    def test_add_route_with_query_parameters(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'key': 'value'}
            return elements, kw

        self.config.add_route('query_route', '/query/{param}', pregenerator=pregenerator)
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('query_route', param='test'),
            '/query/test?key=value'
        )

    def _makeRequest(self):
        from pyramid.request import Request
        from webob.multidict import MultiDict
        return Request(environ={'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'})