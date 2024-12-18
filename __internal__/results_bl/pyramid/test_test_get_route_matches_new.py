import unittest
from pyramid.testing import DummyRequest
from pyramid.urldispatch import RoutesMapper

class TestGetRoute(unittest.TestCase):

    def setUp(self):
        self.mapper = RoutesMapper()

    def test_get_route_non_existent(self):
        result = self.mapper.get_route('non_existent')
        self.assertIsNone(result)

    def test_get_route_empty_string(self):
        result = self.mapper.get_route('')
        self.assertIsNone(result)

    def test_get_route_with_special_characters(self):
        self.mapper.connect('special_route', 'archives/:action/:article')
        result = self.mapper.get_route('special_route')
        self.assertEqual(result.pattern, 'archives/:action/:article')

    def test_get_route_with_numeric_route_name(self):
        self.mapper.connect('123', 'archives/:action/:article')
        result = self.mapper.get_route('123')
        self.assertEqual(result.pattern, 'archives/:action/:article')

    def test_get_route_with_multiple_connections(self):
        self.mapper.connect('first', 'archives/:action/:article')
        self.mapper.connect('second', 'archives/:action/:article/:id')
        result = self.mapper.get_route('second')
        self.assertEqual(result.pattern, 'archives/:action/:article/:id')

    def test_get_route_with_similar_names(self):
        self.mapper.connect('route1', 'archives/:action/:article')
        self.mapper.connect('route1_duplicate', 'archives/:action/:article/:id')
        result = self.mapper.get_route('route1_duplicate')
        self.assertEqual(result.pattern, 'archives/:action/:article/:id')