import unittest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):
    def setUp(self):
        self.request = self._makeOne()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)
        self.request.script_name = ''

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
        self.assertEqual(result, '/1/2/3?a=1')

    def test_route_path_with_anchor(self):
        result = self.request.route_path('flub', _anchor='foo')
        self.assertEqual(result, '/1/2/3#foo')

    def test_route_path_with_query_and_anchor(self):
        result = self.request.route_path('flub', a=1, _anchor='foo')
        self.assertEqual(result, '/1/2/3?a=1#foo')

    def test_route_path_with_empty_route_name(self):
        with self.assertRaises(ValueError):
            self.request.route_path('')

    def test_route_path_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_path('invalid_route')