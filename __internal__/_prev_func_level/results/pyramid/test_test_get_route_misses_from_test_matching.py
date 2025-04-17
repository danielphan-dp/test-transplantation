import unittest
from pyramid.testing import DummyRequest
from pyramid.urldispatch import RoutesMapper

class TestRoutesMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = RoutesMapper()

    def test_get_route_existing(self):
        self.mapper.add_route('test_route', '/test')
        result = self.mapper.get_route('test_route')
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'test_route')

    def test_get_route_non_existing(self):
        result = self.mapper.get_route('non_existing_route')
        self.assertIsNone(result)

    def test_get_route_with_empty_name(self):
        result = self.mapper.get_route('')
        self.assertIsNone(result)

    def test_get_route_with_none_name(self):
        result = self.mapper.get_route(None)
        self.assertIsNone(result)

    def test_get_route_with_special_characters(self):
        self.mapper.add_route('special_route', '/test@123')
        result = self.mapper.get_route('special_route')
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'special_route')

    def test_get_route_with_numeric_name(self):
        self.mapper.add_route('123_route', '/123')
        result = self.mapper.get_route('123_route')
        self.assertIsNotNone(result)
        self.assertEqual(result.name, '123_route')

if __name__ == '__main__':
    unittest.main()