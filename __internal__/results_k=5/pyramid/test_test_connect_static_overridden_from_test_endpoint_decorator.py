import unittest
from pyramid.urldispatch import RoutesMapper

class TestConnectMethod(unittest.TestCase):
    def setUp(self):
        self.mapper = RoutesMapper()

    def test_connect_with_no_routes(self):
        result = self.mapper.connect('foo')
        self.assertIsNone(result)

    def test_connect_with_single_route(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article')

    def test_connect_with_multiple_routes(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

    def test_connect_static_route(self):
        self.mapper.connect('foo', 'archives/:action/:article', static=True)
        self.assertEqual(len(self.mapper.routelist), 0)
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article')

    def test_connect_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.mapper.connect('foo', '')

    def test_connect_overwrite_existing_route(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

if __name__ == '__main__':
    unittest.main()