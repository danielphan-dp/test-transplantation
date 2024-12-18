import unittest
from pyramid.testing import DummyRequest
from pyramid.urldispatch import RoutesMapper

class TestConnectMethod(unittest.TestCase):

    def setUp(self):
        self.mapper = RoutesMapper()

    def test_connect_with_no_routes(self):
        self.assertEqual(len(self.mapper.routes), 0)
        self.mapper.connect('foo', 'archives/:action/:article')
        self.assertEqual(len(self.mapper.routes), 1)

    def test_connect_with_existing_route(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

    def test_connect_static_with_different_patterns(self):
        self.mapper.connect('foo', 'archives/:action/:article', static=True)
        self.assertEqual(len(self.mapper.routelist), 0)
        self.mapper.connect('foo', 'archives/:action/:article2', static=True)
        self.assertEqual(len(self.mapper.routelist), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

    def test_connect_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.mapper.connect('foo', '')

    def test_connect_overwrite_existing_route(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

    def test_connect_multiple_routes(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('bar', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routes), 2)
        self.assertIn('foo', self.mapper.routes)
        self.assertIn('bar', self.mapper.routes)

if __name__ == '__main__':
    unittest.main()