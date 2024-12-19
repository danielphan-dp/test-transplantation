import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'QUERY_STRING': 'la=La%20Pe%C3%B1a',
            'wsgi.url_scheme': 'http',
        }
        self.inst = DummyRequest(self.environ)

    def test_route_url_with_no_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/?')

    def test_route_url_with_empty_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub', '')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/?')

    def test_route_url_with_query_params(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub', a=1, b=2)
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1&b=2')

    def test_route_url_with_anchor(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub', _anchor='foo')
        self.assertEqual(result, 'http://example.com:5432/1/2/3#foo')

    def test_route_url_with_multiple_query_params(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub', a=1, b=2, c=3)
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1&b=2&c=3')

    def test_route_url_with_no_route(self):
        mapper = DummyRoutesMapper(route=None)
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(ValueError):
            self.inst.route_url('nonexistent_route')

    def test_route_url_with_invalid_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.inst.registry.registerUtility(mapper, IRoutesMapper)
        result = self.inst.route_url('flub', None)
        self.assertEqual(result, 'http://example.com:5432/1/2/3/None?')

if __name__ == '__main__':
    unittest.main()