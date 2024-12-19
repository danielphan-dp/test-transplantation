import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):

    def setUp(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'QUERY_STRING': 'la=La%20Pe%C3%B1a',
            'wsgi.url_scheme': 'http',
        }
        self.request = DummyRequest(environ)

    def test_route_path_with_no_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub')
        self.assertEqual(result, '/')

    def test_route_path_with_empty_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/empty'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', '')
        self.assertEqual(result, '/empty/')

    def test_route_path_with_special_characters(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/special/!@#$%^&*()'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', 'special', '!@#$%^&*()')
        self.assertEqual(result, '/special/!@#$%^&*()')

    def test_route_path_with_large_number_of_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/many/elements'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', *['elem' + str(i) for i in range(100)])
        self.assertEqual(result, '/many/elements/' + '/'.join(['elem' + str(i) for i in range(100)]))

    def test_route_path_with_query_parameters(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/query'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', a=1, b=2)
        self.assertEqual(result, '/query?a=1&b=2')

    def test_route_path_with_anchor(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/anchor'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', _anchor='section1')
        self.assertEqual(result, '/anchor#section1')

    def test_route_path_with_multiple_query_parameters(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/multiquery'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_path('flub', a=1, b=2, c=3)
        self.assertEqual(result, '/multiquery?a=1&b=2&c=3')