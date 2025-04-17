import unittest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.request = self._makeOne()
        self.mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'route url')

    def test_route_url_with_single_element(self):
        result = self.request.route_url('flub', 'element1')
        self.assertEqual(result, 'route url')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'route url')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url(
            'flub',
            'element1',
            _query={'key': 'value'}
        )
        self.assertEqual(result, 'route url')

    def test_route_url_with_anchor(self):
        result = self.request.route_url(
            'flub',
            'element1',
            _anchor='anchor'
        )
        self.assertEqual(result, 'route url')

    def test_route_url_with_app_url(self):
        result = self.request.route_url(
            'flub',
            'element1',
            _app_url='http://example.com'
        )
        self.assertEqual(result, 'route url')

    def test_route_url_with_all_parameters(self):
        result = self.request.route_url(
            'flub',
            'element1',
            _app_url='http://example.com',
            _anchor='anchor',
            _query={'q': '1'}
        )
        self.assertEqual(result, 'route url')

    def test_route_url_with_invalid_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

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