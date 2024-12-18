import unittest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):
    def setUp(self):
        self.request = self._makeOne()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_path_with_no_elements(self):
        result = self.request.route_path('flub')
        self.assertEqual(result, '/1/2/3')

    def test_route_path_with_single_element(self):
        result = self.request.route_path('flub', 'extra1')
        self.assertEqual(result, '/1/2/3/extra1')

    def test_route_path_with_multiple_elements(self):
        result = self.request.route_path('flub', 'extra1', 'extra2')
        self.assertEqual(result, '/1/2/3/extra1/extra2')

    def test_route_path_with_query_params(self):
        result = self.request.route_path('flub', a=1, b=2)
        self.assertEqual(result, '/1/2/3?a=1&b=2')

    def test_route_path_with_anchor(self):
        result = self.request.route_path('flub', _anchor='foo')
        self.assertEqual(result, '/1/2/3#foo')

    def test_route_path_with_script_name(self):
        self.request.script_name = '/foo'
        result = self.request.route_path('flub', 'extra1', 'extra2', _query={'a': 1}, _anchor='foo')
        self.assertEqual(result, '/foo/1/2/3/extra1/extra2?a=1#foo')

    def test_route_path_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_path('invalid_route')

    def _makeOne(self):
        from pyramid.request import Request
        return Request.blank('/')

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result