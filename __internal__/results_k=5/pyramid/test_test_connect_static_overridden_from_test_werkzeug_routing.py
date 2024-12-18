import unittest
from pyramid.urldispatch import RoutesMapper

class TestConnectMethod(unittest.TestCase):

    def setUp(self):
        self.mapper = RoutesMapper()

    def test_connect_with_static(self):
        self.mapper.connect('foo', 'archives/:action/:article', static=True)
        self.assertEqual(len(self.mapper.routelist), 0)
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article')

    def test_connect_with_different_article(self):
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routelist), 1)
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')
        self.assertEqual(self.mapper.routelist[0].pattern, 'archives/:action/:article2')

    def test_connect_with_no_routes(self):
        self.assertEqual(len(self.mapper.routes), 0)

    def test_connect_overwrite_existing_route(self):
        self.mapper.connect('foo', 'archives/:action/:article')
        self.mapper.connect('foo', 'archives/:action/:article2')
        self.assertEqual(len(self.mapper.routes), 1)
        self.assertEqual(self.mapper.routes['foo'].pattern, 'archives/:action/:article2')

    def test_connect_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.mapper.connect('foo', '')

if __name__ == '__main__':
    unittest.main()