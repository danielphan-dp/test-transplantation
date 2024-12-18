import unittest
from pyramid.testing import DummyRequest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_without_prefix(self):
        self.config.add_route('test_route', '/test')
        request = DummyRequest()
        self.assertEqual(request.route_url('test_route'), 'http://localhost/test')

    def test_add_route_with_empty_args(self):
        self.config.add_route('empty_route', '')
        request = DummyRequest()
        self.assertEqual(request.route_url('empty_route'), 'http://localhost/')

    def test_add_route_with_query_params(self):
        self.config.add_route('query_route', '/query')
        request = DummyRequest()
        self.assertEqual(request.route_url('query_route', _query={'param': 'value'}), 'http://localhost/query?param=value')

    def test_add_route_with_dynamic_segment(self):
        self.config.add_route('dynamic_route', '/dynamic/{id}')
        request = DummyRequest()
        self.assertEqual(request.route_url('dynamic_route', id='123'), 'http://localhost/dynamic/123')

    def test_add_route_with_invalid_name(self):
        with self.assertRaises(KeyError):
            request = DummyRequest()
            request.route_url('non_existent_route')

    def test_add_route_with_multiple_routes(self):
        self.config.add_route('first_route', '/first')
        self.config.add_route('second_route', '/second')
        request = DummyRequest()
        self.assertEqual(request.route_url('first_route'), 'http://localhost/first')
        self.assertEqual(request.route_url('second_route'), 'http://localhost/second')