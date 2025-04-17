import unittest
from pyramid.urldispatch import RoutesMapper, Route

class TestGetRoute(unittest.TestCase):

    def setUp(self):
        self.mapper = RoutesMapper()
        self.route_name = 'test_route'
        self.route_pattern = 'archives/:action/:article'
        self.mapper.connect(self.route_name, self.route_pattern)

    def test_get_route_returns_correct_route(self):
        result = self.mapper.get_route(self.route_name)
        self.assertEqual(result.pattern, self.route_pattern)

    def test_get_route_with_non_existent_route(self):
        with self.assertRaises(KeyError):
            self.mapper.get_route('non_existent_route')

    def test_get_route_with_empty_route_name(self):
        with self.assertRaises(KeyError):
            self.mapper.get_route('')

    def test_get_route_with_special_characters(self):
        special_route_name = 'route_with_special_chars!@#'
        special_route_pattern = 'archives/:action/:article/:id'
        self.mapper.connect(special_route_name, special_route_pattern)
        result = self.mapper.get_route(special_route_name)
        self.assertEqual(result.pattern, special_route_pattern)

    def test_get_route_multiple_routes(self):
        another_route_name = 'another_route'
        another_route_pattern = 'archives/:action/:id'
        self.mapper.connect(another_route_name, another_route_pattern)
        result = self.mapper.get_route(another_route_name)
        self.assertEqual(result.pattern, another_route_pattern)

if __name__ == '__main__':
    unittest.main()