import unittest
from pyramid.config import Configurator
from pyramid.request import Request

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_without_prefix(self):
        self.config.add_route('test_route', '/test')
        request = self._makeRequest('/')
        self.assertEqual(request.route_url('test_route'), 'http://localhost/test')

    def test_add_route_with_empty_args(self):
        self.config.add_route('empty_route', '')
        request = self._makeRequest('/')
        self.assertEqual(request.route_url('empty_route'), 'http://localhost/')

    def test_add_route_with_query_params(self):
        self.config.add_route('query_route', '/query')
        request = self._makeRequest('/query?param=value')
        self.assertEqual(request.route_url('query_route', _query={'param': 'value'}), 'http://localhost/query?param=value')

    def test_add_route_with_dynamic_segment(self):
        self.config.add_route('dynamic_route', '/dynamic/{id}')
        request = self._makeRequest('/dynamic/123')
        self.assertEqual(request.route_url('dynamic_route', id='123'), 'http://localhost/dynamic/123')

    def test_add_route_with_invalid_name(self):
        with self.assertRaises(KeyError):
            request = self._makeRequest('/')
            request.route_url('non_existent_route')

    def _makeRequest(self, path):
        request = Request.blank(path)
        self.config.begin(request)
        return request

if __name__ == '__main__':
    unittest.main()